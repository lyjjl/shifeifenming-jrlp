import type { CharacterData } from './api';
import {
  CONFIG_KEYS,
  getCleanApiUrl,
  getDailyLimit,
  getTemplate,
  isUseBase64CQ,
  isUseSealCode,
} from './config';
import { getMarriedDays, getRemainingDays } from './marriage';
import type { MarriageData } from './storage';
import { getUserIdFromCtx } from './storage';
import { buildAvatarTag, processTemplate, sanitizeExternalValue } from './template';

export function formatImageTag(ext: seal.ExtInfo, data: CharacterData): string {
  const baseUrl = getCleanApiUrl(ext);
  const rawSub = data.image_sub ?? '';
  const subPath = rawSub && !rawSub.startsWith('/') ? `/${rawSub}` : rawSub;

  // Sanitize external values to prevent seal.format() injection
  const safeUrl = sanitizeExternalValue(`${baseUrl}${subPath}`);

  if (isUseSealCode(ext)) {
    return `[图:${safeUrl}]`;
  }
  if (isUseBase64CQ(ext) && data.image_base64) {
    const safeBase64 = sanitizeExternalValue(data.image_base64);
    return `[CQ:image,file=base64://${safeBase64}]`;
  }
  return `[CQ:image,file=${safeUrl}]`;
}

function buildBaseVars(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  data: CharacterData,
): Record<string, string> {
  return {
    老婆图片: formatImageTag(ext, data),
    老婆名字: sanitizeExternalValue(data.filename || '神秘角色'),
    玩家: '{$t玩家}',
    次数上限: String(getDailyLimit(ext)),
    用户头像: buildAvatarTag(getUserIdFromCtx(ctx)),
  };
}

export function formatJrlpResponse(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  data: CharacterData,
): string {
  const templates = getTemplate(ext, CONFIG_KEYS.TPL_JRLP);
  const vars = buildBaseVars(ctx, ext, data);
  return processTemplate(templates, vars, ctx, ext);
}

export function formatHlpResponse(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  data: CharacterData,
): string {
  const templates = getTemplate(ext, CONFIG_KEYS.TPL_HLP);
  const vars = buildBaseVars(ctx, ext, data);
  return processTemplate(templates, vars, ctx, ext);
}

export function formatHlpLimitResponse(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  data: CharacterData,
): string {
  const templates = getTemplate(ext, CONFIG_KEYS.TPL_HLP_LIMIT);
  const vars = buildBaseVars(ctx, ext, data);
  return processTemplate(templates, vars, ctx, ext);
}

export function formatMarryResponse(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  data: CharacterData,
): string {
  const templates = getTemplate(ext, CONFIG_KEYS.TPL_MARRY);
  const vars = buildBaseVars(ctx, ext, data);
  return processTemplate(templates, vars, ctx, ext);
}

export function formatMarriedStatusResponse(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  data: CharacterData,
  marriage: MarriageData,
  durationDays: number,
): string {
  const templates = getTemplate(ext, CONFIG_KEYS.TPL_MARRIED_STATUS);
  const vars = {
    ...buildBaseVars(ctx, ext, data),
    天数: String(getMarriedDays(marriage)),
    剩余天数: String(getRemainingDays(marriage, durationDays)),
  };
  return processTemplate(templates, vars, ctx, ext);
}

export function formatDivorceResponse(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  wifeName: string,
): string {
  const templates = getTemplate(ext, CONFIG_KEYS.TPL_DIVORCE);
  const vars: Record<string, string> = {
    玩家: '{$t玩家}',
    老婆名字: sanitizeExternalValue(wifeName || '神秘角色'),
    用户头像: buildAvatarTag(getUserIdFromCtx(ctx)),
  };
  return processTemplate(templates, vars, ctx, ext);
}

export function formatSimpleTemplate(
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
  configKey: string,
): string {
  const templates = getTemplate(ext, configKey);
  const vars: Record<string, string> = {
    玩家: '{$t玩家}',
    用户头像: buildAvatarTag(getUserIdFromCtx(ctx)),
  };
  return processTemplate(templates, vars, ctx, ext);
}
