import type { CharacterData } from './api';
import { getMarriageDuration } from './config';
import { logDebug } from './logger';
import {
  MS_PER_DAY,
  type MarriageData,
  type WifeData,
  getAllUserEntries,
  getUserData,
  getUserIdFromCtx,
  removeUserMarriage,
  saveStorage,
  setUserData,
} from './storage';

export function isMarried(ctx: seal.MsgContext): boolean {
  const user = getUserData(getUserIdFromCtx(ctx));
  return user.marriage !== null;
}

export function getMarriage(ctx: seal.MsgContext): MarriageData | null {
  const user = getUserData(getUserIdFromCtx(ctx));
  return user.marriage;
}

export function getMarriedDays(marriage: MarriageData): number {
  const elapsed = Date.now() - marriage.startTimestamp;
  return Math.max(1, Math.floor(elapsed / MS_PER_DAY));
}

export function getRemainingDays(marriage: MarriageData, durationDays: number): number {
  const elapsed = Date.now() - marriage.startTimestamp;
  const remaining = durationDays - Math.floor(elapsed / MS_PER_DAY);
  return Math.max(0, remaining);
}

export function isMarriageExpired(marriage: MarriageData, durationDays: number): boolean {
  return getRemainingDays(marriage, durationDays) <= 0;
}

export function marry(ctx: seal.MsgContext, wife: CharacterData): void {
  const userId = getUserIdFromCtx(ctx);
  const user = getUserData(userId);
  user.marriage = {
    wife: {
      imageSub: wife.image_sub ?? '',
      name: wife.filename ?? '',
    },
    startTimestamp: Date.now(),
  };
  setUserData(userId, user);
  saveStorage();
}

export function divorce(ctx: seal.MsgContext): WifeData | null {
  const userId = getUserIdFromCtx(ctx);
  const user = getUserData(userId);
  const wife = user.marriage?.wife ?? null;
  user.marriage = null;
  setUserData(userId, user);
  saveStorage();
  return wife;
}

export function checkAndClearExpiry(ctx: seal.MsgContext, ext: seal.ExtInfo): boolean {
  const userId = getUserIdFromCtx(ctx);
  const user = getUserData(userId);
  if (!user.marriage) return false;

  const duration = getMarriageDuration(ext);
  if (isMarriageExpired(user.marriage, duration)) {
    logDebug(ext, `用户 ${userId} 婚姻已过期，惰性清除`);
    user.marriage = null;
    setUserData(userId, user);
    saveStorage();
    return true;
  }
  return false;
}

export function cleanExpiredMarriages(ext: seal.ExtInfo): void {
  const duration = getMarriageDuration(ext);
  let cleaned = 0;

  for (const [userId, user] of getAllUserEntries()) {
    if (user.marriage && isMarriageExpired(user.marriage, duration)) {
      removeUserMarriage(userId);
      cleaned++;
    }
  }

  if (cleaned > 0) {
    logDebug(ext, `每日清理：移除 ${cleaned} 个过期婚姻`);
    saveStorage();
  }
}
