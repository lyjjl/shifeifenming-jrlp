import type { CharacterData } from './api';
import { logDebug } from './logger';
import {
  type WifeData,
  getCurrentDayId,
  getUserData,
  getUserIdFromCtx,
  saveStorage,
  setUserData,
} from './storage';

export function resetIfNewDay(ctx: seal.MsgContext, ext: seal.ExtInfo): void {
  const userId = getUserIdFromCtx(ctx);
  const user = getUserData(userId);
  const currentDay = getCurrentDayId();

  if (user.lastDayId !== currentDay) {
    logDebug(ext, `日期变更 (${user.lastDayId} -> ${currentDay})，重置用户 ${userId}`);
    user.lastDayId = currentDay;
    user.dailyCount = 0;
    user.wife = null;
    setUserData(userId, user);
    saveStorage();
  }
}

export function getDailyCount(ctx: seal.MsgContext): number {
  const user = getUserData(getUserIdFromCtx(ctx));
  return user.dailyCount;
}

export function incrementDailyCount(ctx: seal.MsgContext): void {
  const userId = getUserIdFromCtx(ctx);
  const user = getUserData(userId);
  user.dailyCount += 1;
  setUserData(userId, user);
  saveStorage();
}

export function getCachedCharacter(ctx: seal.MsgContext): CharacterData | null {
  const user = getUserData(getUserIdFromCtx(ctx));
  if (!user.wife) return null;
  return wifeDataToCharacter(user.wife);
}

export function cacheCharacter(ctx: seal.MsgContext, data: CharacterData): void {
  const userId = getUserIdFromCtx(ctx);
  const user = getUserData(userId);
  user.wife = characterToWifeData(data);
  setUserData(userId, user);
  saveStorage();
}

function characterToWifeData(data: CharacterData): WifeData {
  return {
    imageSub: data.image_sub ?? '',
    name: data.filename ?? '',
  };
}

function wifeDataToCharacter(wife: WifeData): CharacterData {
  return {
    image_sub: wife.imageSub,
    filename: wife.name,
  };
}
