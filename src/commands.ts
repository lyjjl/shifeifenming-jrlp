import { getCharacterData, getStatus } from './api';
import {
  CONFIG_KEYS,
  getDailyLimit,
  getMarriageDuration,
  isUseBase64CQ,
  isUseSealCode,
} from './config';
import {
  formatDivorceResponse,
  formatHlpLimitResponse,
  formatHlpResponse,
  formatJrlpResponse,
  formatMarriedStatusResponse,
  formatMarryResponse,
  formatSimpleTemplate,
} from './formatter';
import { logError } from './logger';
import { checkAndClearExpiry, divorce, getMarriage, isMarried, marry } from './marriage';
import {
  cacheCharacter,
  getCachedCharacter,
  getDailyCount,
  incrementDailyCount,
  resetIfNewDay,
} from './state';

function validateConfig(ctx: seal.MsgContext, msg: seal.Message, ext: seal.ExtInfo): boolean {
  if (isUseSealCode(ext) && isUseBase64CQ(ext)) {
    seal.replyToSender(
      ctx,
      msg,
      '【插件配置错误】不能同时启用 useSealCode 和 useBase64CQ，请联系管理员修改插件配置。',
    );
    return false;
  }
  return true;
}

async function handleJrlp(
  ctx: seal.MsgContext,
  msg: seal.Message,
  ext: seal.ExtInfo,
): Promise<void> {
  resetIfNewDay(ctx, ext);
  checkAndClearExpiry(ctx, ext);
  if (!validateConfig(ctx, msg, ext)) return;

  const marriage = getMarriage(ctx);
  if (marriage) {
    const wifeData = {
      image_sub: marriage.wife.imageSub,
      filename: marriage.wife.name,
    };
    const duration = getMarriageDuration(ext);
    seal.replyToSender(
      ctx,
      msg,
      formatMarriedStatusResponse(ctx, ext, wifeData, marriage, duration),
    );
    return;
  }

  const todayCount = getDailyCount(ctx);
  if (todayCount > 0) {
    const cached = getCachedCharacter(ctx);
    if (cached) {
      seal.replyToSender(ctx, msg, formatJrlpResponse(ctx, ext, cached));
      return;
    }
  }

  const data = await getCharacterData(ext, isUseBase64CQ(ext));
  if (!data) {
    seal.replyToSender(ctx, msg, '获取老婆失败，后端暂时不可用。');
    return;
  }

  cacheCharacter(ctx, data);
  incrementDailyCount(ctx);
  seal.replyToSender(ctx, msg, formatJrlpResponse(ctx, ext, data));
}

async function handleHlp(
  ctx: seal.MsgContext,
  msg: seal.Message,
  ext: seal.ExtInfo,
): Promise<void> {
  resetIfNewDay(ctx, ext);
  checkAndClearExpiry(ctx, ext);
  if (!validateConfig(ctx, msg, ext)) return;

  if (isMarried(ctx)) {
    seal.replyToSender(ctx, msg, formatSimpleTemplate(ctx, ext, CONFIG_KEYS.TPL_HLP_BLOCKED));
    return;
  }

  const todayCount = getDailyCount(ctx);
  if (todayCount === 0) {
    seal.replyToSender(ctx, msg, formatSimpleTemplate(ctx, ext, CONFIG_KEYS.TPL_NO_WIFE_MARRY));
    return;
  }

  const limit = getDailyLimit(ext);
  if (todayCount >= limit) {
    const cached = getCachedCharacter(ctx);
    if (cached) {
      seal.replyToSender(ctx, msg, formatHlpLimitResponse(ctx, ext, cached));
    }
    return;
  }

  const data = await getCharacterData(ext, isUseBase64CQ(ext));
  if (!data) {
    seal.replyToSender(ctx, msg, '获取老婆失败，后端暂时不可用。');
    return;
  }

  cacheCharacter(ctx, data);
  incrementDailyCount(ctx);
  seal.replyToSender(ctx, msg, formatHlpResponse(ctx, ext, data));
}

function handleMarry(ctx: seal.MsgContext, msg: seal.Message, ext: seal.ExtInfo): void {
  resetIfNewDay(ctx, ext);
  checkAndClearExpiry(ctx, ext);
  if (!validateConfig(ctx, msg, ext)) return;

  const marriage = getMarriage(ctx);
  if (marriage) {
    const wifeData = {
      image_sub: marriage.wife.imageSub,
      filename: marriage.wife.name,
    };
    const duration = getMarriageDuration(ext);
    seal.replyToSender(
      ctx,
      msg,
      formatMarriedStatusResponse(ctx, ext, wifeData, marriage, duration),
    );
    return;
  }

  const cached = getCachedCharacter(ctx);
  if (!cached) {
    seal.replyToSender(ctx, msg, formatSimpleTemplate(ctx, ext, CONFIG_KEYS.TPL_NO_WIFE_MARRY));
    return;
  }

  marry(ctx, cached);
  seal.replyToSender(ctx, msg, formatMarryResponse(ctx, ext, cached));
}

function handleDivorce(ctx: seal.MsgContext, msg: seal.Message, ext: seal.ExtInfo): void {
  resetIfNewDay(ctx, ext);
  checkAndClearExpiry(ctx, ext);
  if (!validateConfig(ctx, msg, ext)) return;

  if (!isMarried(ctx)) {
    seal.replyToSender(ctx, msg, formatSimpleTemplate(ctx, ext, CONFIG_KEYS.TPL_NOT_MARRIED));
    return;
  }

  const wife = divorce(ctx);
  const wifeName = wife?.name ?? '神秘角色';
  seal.replyToSender(ctx, msg, formatDivorceResponse(ctx, ext, wifeName));
}

export function registerCommands(ext: seal.ExtInfo): void {
  const cmdJrlp = seal.ext.newCmdItemInfo();
  cmdJrlp.name = 'jrlp';
  cmdJrlp.help =
    '.jrlp 查看今日老婆\n.jrlp status 查看后端状态\n.jrlp 结婚 与今日老婆结婚\n.jrlp 离婚 解除婚姻关系';

  cmdJrlp.solve = async (ctx, msg, cmdArgs) => {
    const subCmd = cmdArgs.getArgN(1);

    switch (subCmd) {
      case 'status': {
        const status = await getStatus(ext);
        if (!status) {
          seal.replyToSender(ctx, msg, '无法连接到后端服务');
          return seal.ext.newCmdExecuteResult(true);
        }
        const { system_metrics: sys, image_statistics: img } = status;
        const mem = sys.memory_usage;
        seal.replyToSender(
          ctx,
          msg,
          `API 状态: ${status.service_availability}\n` +
            `CPU: ${sys.cpu_usage_percent}%\n` +
            `RAM: ${mem.used_gb}/${mem.total_gb} (${mem.percent}%)\n` +
            `ImgNum: ${img.total_count}`,
        );
        return seal.ext.newCmdExecuteResult(true);
      }
      case '结婚':
        handleMarry(ctx, msg, ext);
        return seal.ext.newCmdExecuteResult(true);
      case '离婚':
        handleDivorce(ctx, msg, ext);
        return seal.ext.newCmdExecuteResult(true);
      default:
        await handleJrlp(ctx, msg, ext);
        return seal.ext.newCmdExecuteResult(true);
    }
  };

  const cmdHlp = seal.ext.newCmdItemInfo();
  cmdHlp.name = 'hlp';
  cmdHlp.help = '.hlp 换老婆（每日有限次数）';

  cmdHlp.solve = async (ctx, msg) => {
    await handleHlp(ctx, msg, ext);
    return seal.ext.newCmdExecuteResult(true);
  };

  ext.cmdMap.jrlp = cmdJrlp;
  ext.cmdMap.今日老婆 = cmdJrlp;
  ext.cmdMap.hlp = cmdHlp;
  ext.cmdMap.换老婆 = cmdHlp;
}

export function registerNonCommandHandler(ext: seal.ExtInfo): void {
  ext.onNotCommandReceived = async (ctx, msg) => {
    try {
      const text = msg.message.replace(/\[CQ:at,qq=.*?]\s*/, '').trim();

      if (['jrlp', '今日老婆'].includes(text)) {
        await handleJrlp(ctx, msg, ext);
      } else if (['hlp', '换老婆'].includes(text)) {
        await handleHlp(ctx, msg, ext);
      }
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : String(e);
      logError(`onNotCommandReceived 异常: ${message}`);
    }
  };
}
