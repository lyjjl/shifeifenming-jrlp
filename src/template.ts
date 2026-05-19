import { isNoFormat } from './config';

function sanitizeForFormat(value: string): string {
  return value.replace(/\{/g, '\uFF5B').replace(/\}/g, '\uFF5D');
}

export function sanitizeExternalValue(value: string): string {
  return sanitizeForFormat(value);
}

export function processTemplate(
  templates: string[],
  vars: Record<string, string>,
  ctx: seal.MsgContext,
  ext: seal.ExtInfo,
): string {
  if (templates.length === 0) return '';

  const selected = templates[Math.floor(Math.random() * templates.length)];

  const replaced = selected.replace(/\{\{(.+?)\}\}/g, (_match, key: string) => {
    const trimmed = key.trim();
    return trimmed in vars ? vars[trimmed] : `{{${trimmed}}}`;
  });

  return isNoFormat(ext) ? replaced : seal.format(ctx, replaced);
}

export function buildAvatarTag(userId: string): string {
  if (!userId.startsWith('QQ:')) return '';
  const qq = userId.slice(3);
  return `[CQ:image,file=https://q1.qlogo.cn/g?b=qq&nk=${qq}&s=640]`;
}
