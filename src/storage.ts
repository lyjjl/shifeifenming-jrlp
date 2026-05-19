import { logDebug, logError } from './logger';

// ─── Data Types ───────────────────────────────────────────────────────────────

export interface WifeData {
  imageSub: string;
  name: string;
}

export interface MarriageData {
  wife: WifeData;
  startTimestamp: number;
}

export interface UserData {
  lastDayId: number;
  dailyCount: number;
  wife: WifeData | null;
  marriage: MarriageData | null;
}

export interface GlobalData {
  version: number;
  users: Record<string, UserData>;
}

// ─── Constants ────────────────────────────────────────────────────────────────

const STORAGE_KEY = 'jrlp_global';
const CURRENT_VERSION = 2;

export const MS_PER_DAY = 86_400_000;

const UTC8_OFFSET_MS = 8 * 60 * 60 * 1000;

// ─── Module State ─────────────────────────────────────────────────────────────

let globalData: GlobalData = { version: CURRENT_VERSION, users: {} };
let extRef: seal.ExtInfo | null = null;

// ─── Helpers ──────────────────────────────────────────────────────────────────

/** Day ID based on UTC+8 — day boundary is midnight Beijing time */
export function getCurrentDayId(): number {
  return Math.floor((Date.now() + UTC8_OFFSET_MS) / MS_PER_DAY);
}

function createEmptyUserData(): UserData {
  return {
    lastDayId: 0,
    dailyCount: 0,
    wife: null,
    marriage: null,
  };
}

// ─── Validation ───────────────────────────────────────────────────────────────

function isValidWifeData(data: unknown): data is WifeData {
  if (typeof data !== 'object' || data === null) return false;
  const obj = data as Record<string, unknown>;
  return typeof obj.imageSub === 'string' && typeof obj.name === 'string';
}

function isValidMarriageData(data: unknown): data is MarriageData {
  if (typeof data !== 'object' || data === null) return false;
  const obj = data as Record<string, unknown>;
  return (
    typeof obj.startTimestamp === 'number' &&
    Number.isFinite(obj.startTimestamp) &&
    isValidWifeData(obj.wife)
  );
}

function isValidUserData(data: unknown): data is UserData {
  if (typeof data !== 'object' || data === null) return false;
  const obj = data as Record<string, unknown>;
  if (typeof obj.lastDayId !== 'number' || !Number.isFinite(obj.lastDayId)) return false;
  if (typeof obj.dailyCount !== 'number' || !Number.isFinite(obj.dailyCount)) return false;
  if (obj.wife !== null && !isValidWifeData(obj.wife)) return false;
  if (obj.marriage !== null && !isValidMarriageData(obj.marriage)) return false;
  return true;
}

function isValidGlobalData(data: unknown): data is GlobalData {
  if (typeof data !== 'object' || data === null) return false;
  const obj = data as Record<string, unknown>;
  if (typeof obj.version !== 'number') return false;
  if (typeof obj.users !== 'object' || obj.users === null) return false;
  return true;
}

// ─── Migration ────────────────────────────────────────────────────────────────

/** v1 → v2: Remove imageBase64 field from WifeData */
function migrateData(data: GlobalData): GlobalData {
  if (data.version < 2) {
    for (const userId of Object.keys(data.users)) {
      const user = data.users[userId];
      if (user.wife) {
        const legacy = user.wife as unknown as Record<string, unknown>;
        user.wife = {
          imageSub: String(legacy.imageSub ?? ''),
          name: String(legacy.name ?? ''),
        };
      }
      if (user.marriage?.wife) {
        const legacy = user.marriage.wife as unknown as Record<string, unknown>;
        user.marriage.wife = {
          imageSub: String(legacy.imageSub ?? ''),
          name: String(legacy.name ?? ''),
        };
      }
    }
    data.version = 2;
  }
  return data;
}

// ─── Initialization ───────────────────────────────────────────────────────────

export function initStorage(ext: seal.ExtInfo): void {
  extRef = ext;
  const raw = ext.storageGet(STORAGE_KEY);

  if (!raw) {
    logDebug(ext, '未找到存储数据，初始化空数据');
    globalData = { version: CURRENT_VERSION, users: {} };
    return;
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (isValidGlobalData(parsed)) {
      globalData = parsed.version < CURRENT_VERSION ? migrateData(parsed) : parsed;

      const validUsers: Record<string, UserData> = {};
      for (const [userId, userData] of Object.entries(globalData.users)) {
        if (isValidUserData(userData)) {
          validUsers[userId] = userData;
        } else {
          logDebug(ext, `用户 ${userId} 数据无效，已跳过`);
        }
      }
      globalData.users = validUsers;

      logDebug(ext, `加载存储数据成功，用户数: ${Object.keys(globalData.users).length}`);

      if (parsed.version < CURRENT_VERSION) {
        saveStorage();
        logDebug(ext, `数据已从 v${parsed.version} 迁移到 v${CURRENT_VERSION}`);
      }
    } else {
      logError('存储数据格式无效，重置为空数据');
      globalData = { version: CURRENT_VERSION, users: {} };
    }
  } catch {
    logError('存储数据解析失败，重置为空数据');
    globalData = { version: CURRENT_VERSION, users: {} };
  }
}

// ─── Persistence ──────────────────────────────────────────────────────────────

export function saveStorage(): void {
  if (!extRef) {
    logError('saveStorage 调用时 extRef 未初始化');
    return;
  }
  try {
    extRef.storageSet(STORAGE_KEY, JSON.stringify(globalData));
  } catch {
    logError('存储数据保存失败');
  }
}

// ─── User Data Access ─────────────────────────────────────────────────────────

export function getUserData(userId: string): UserData {
  if (!globalData.users[userId]) {
    globalData.users[userId] = createEmptyUserData();
  }
  return globalData.users[userId];
}

export function setUserData(userId: string, data: UserData): void {
  globalData.users[userId] = data;
}

export function getAllUserEntries(): [string, UserData][] {
  return Object.entries(globalData.users);
}

/** Removes marriage data in memory only. Caller MUST call saveStorage() after. */
export function removeUserMarriage(userId: string): void {
  const user = globalData.users[userId];
  if (user) {
    user.marriage = null;
  }
}

// ─── Utility ──────────────────────────────────────────────────────────────────

export function getUserIdFromCtx(ctx: seal.MsgContext): string {
  return ctx.player.userId;
}
