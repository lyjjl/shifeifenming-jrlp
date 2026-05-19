export const CONFIG_KEYS = {
  DEBUG: 'debug',
  USE_SEAL_CODE: 'useSealCode',
  USE_BASE64_CQ: 'useBase64CQ',
  NO_FORMAT: 'noFormat',
  API_URL: 'api_url',
  DAILY_HLP_LIMIT: 'daily_hlp_limit',
  RETRY_TIMES: 'retry_times',
  RETRY_INTERVAL: 'retry_interval',
  MARRIAGE_DURATION: 'marriage_duration',
  TPL_JRLP: 'tpl_jrlp',
  TPL_HLP: 'tpl_hlp',
  TPL_HLP_LIMIT: 'tpl_hlp_limit',
  TPL_MARRY: 'tpl_marry',
  TPL_MARRIED_STATUS: 'tpl_married_status',
  TPL_DIVORCE: 'tpl_divorce',
  TPL_NOT_MARRIED: 'tpl_not_married',
  TPL_NO_WIFE_MARRY: 'tpl_no_wife_marry',
  TPL_HLP_BLOCKED: 'tpl_hlp_blocked',
} as const;

export function registerConfigs(ext: seal.ExtInfo): void {
  seal.ext.registerBoolConfig(ext, CONFIG_KEYS.DEBUG, false, '调试模式 【报告问题前必须启用】');
  seal.ext.registerBoolConfig(ext, CONFIG_KEYS.USE_SEAL_CODE, false, '使用海豹码代替CQ码 不懂别开');
  seal.ext.registerBoolConfig(
    ext,
    CONFIG_KEYS.USE_BASE64_CQ,
    false,
    '使用 base64:// CQ Code 不懂别开',
  );
  seal.ext.registerBoolConfig(ext, CONFIG_KEYS.NO_FORMAT, false, '不执行 format 不懂别开');
  seal.ext.registerStringConfig(
    ext,
    CONFIG_KEYS.API_URL,
    'http://localhost:18428',
    'jrlp 后端地址 [ 结尾有无 / 均可 ]',
  );
  seal.ext.registerIntConfig(ext, CONFIG_KEYS.DAILY_HLP_LIMIT, 5, '每天最多换老婆次数');
  seal.ext.registerIntConfig(ext, CONFIG_KEYS.RETRY_TIMES, 3, 'API失败重试次数');
  seal.ext.registerIntConfig(ext, CONFIG_KEYS.RETRY_INTERVAL, 1000, '重试间隔(ms)');
  seal.ext.registerIntConfig(ext, CONFIG_KEYS.MARRIAGE_DURATION, 7, '结婚维持时间(天)');

  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_JRLP,
    ['{{老婆图片}}\n{{玩家}}今天的老婆是{{老婆名字}}'],
    '今日老婆文案模板（支持多条随机）',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_HLP,
    ['{{老婆图片}}\n{{玩家}}的新老婆是{{老婆名字}}'],
    '换老婆文案模板',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_HLP_LIMIT,
    ['{{老婆图片}}\n{{玩家}}今天的老婆是{{老婆名字}}\n(每天最多换{{次数上限}}次老婆哦)'],
    '换老婆达到上限文案模板',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_MARRY,
    ['{{老婆图片}}\n恭喜{{玩家}}与{{老婆名字}}喜结连理！'],
    '结婚文案模板',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_MARRIED_STATUS,
    ['{{老婆图片}}\n{{玩家}}与{{老婆名字}}已经幸福地生活了{{天数}}天\n(剩余{{剩余天数}}天)'],
    '已婚状态文案模板（jrlp时显示）',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_DIVORCE,
    ['{{玩家}}与{{老婆名字}}的缘分走到了尽头...'],
    '离婚文案模板',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_NOT_MARRIED,
    ['你还没有结婚哦'],
    '未婚时执行离婚的文案',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_NO_WIFE_MARRY,
    ['你还没有今日老婆，先用 .jrlp 获取一位吧'],
    '无老婆时执行结婚的文案',
  );
  seal.ext.registerTemplateConfig(
    ext,
    CONFIG_KEYS.TPL_HLP_BLOCKED,
    ['你已经结婚了，不能换老婆哦！\n如需解除关系请使用 .jrlp 离婚'],
    '婚姻期间换老婆被拒绝的文案',
  );
}

export function getCleanApiUrl(ext: seal.ExtInfo): string {
  const url = seal.ext.getStringConfig(ext, CONFIG_KEYS.API_URL).trim();
  return url.replace(/\/+$/, '');
}

export function isDebugEnabled(ext: seal.ExtInfo): boolean {
  return seal.ext.getBoolConfig(ext, CONFIG_KEYS.DEBUG);
}

export function isUseSealCode(ext: seal.ExtInfo): boolean {
  return seal.ext.getBoolConfig(ext, CONFIG_KEYS.USE_SEAL_CODE);
}

export function isUseBase64CQ(ext: seal.ExtInfo): boolean {
  return seal.ext.getBoolConfig(ext, CONFIG_KEYS.USE_BASE64_CQ);
}

export function isNoFormat(ext: seal.ExtInfo): boolean {
  return seal.ext.getBoolConfig(ext, CONFIG_KEYS.NO_FORMAT);
}

export function getDailyLimit(ext: seal.ExtInfo): number {
  return seal.ext.getIntConfig(ext, CONFIG_KEYS.DAILY_HLP_LIMIT);
}

export function getRetryTimes(ext: seal.ExtInfo): number {
  return seal.ext.getIntConfig(ext, CONFIG_KEYS.RETRY_TIMES);
}

export function getRetryInterval(ext: seal.ExtInfo): number {
  return seal.ext.getIntConfig(ext, CONFIG_KEYS.RETRY_INTERVAL);
}

export function getMarriageDuration(ext: seal.ExtInfo): number {
  return seal.ext.getIntConfig(ext, CONFIG_KEYS.MARRIAGE_DURATION);
}

export function getTemplate(ext: seal.ExtInfo, key: string): string[] {
  return seal.ext.getTemplateConfig(ext, key);
}
