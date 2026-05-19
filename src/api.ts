import { getCleanApiUrl, getRetryInterval, getRetryTimes } from './config';
import { logDebug, logError } from './logger';

export interface CharacterData {
  image_sub?: string;
  image_base64?: string;
  filename?: string;
}

export interface StatusResponse {
  service_availability: string;
  system_metrics: {
    cpu_usage_percent: number;
    memory_usage: {
      used_gb: string;
      total_gb: string;
      percent: string;
    };
  };
  image_statistics: {
    total_count: number;
  };
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isTransientError(status: number): boolean {
  return status >= 500 || status === 408 || status === 429;
}

async function fetchWithRetry(ext: seal.ExtInfo, url: string): Promise<Response | null> {
  const times = getRetryTimes(ext);
  const interval = getRetryInterval(ext);

  for (let i = 0; i < times; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return res;

      if (!isTransientError(res.status)) {
        logDebug(ext, `请求失败 ${res.status}（非瞬态错误），不再重试`);
        return null;
      }
      logDebug(ext, `请求失败 ${res.status}，重试 ${i + 1}/${times}`);
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : String(e);
      logDebug(ext, `网络异常，重试 ${i + 1}/${times}: ${message}`);
    }
    if (i < times - 1) await sleep(interval);
  }
  return null;
}

export async function getCharacterData(
  ext: seal.ExtInfo,
  needBase64 = false,
): Promise<CharacterData | null> {
  const baseUrl = getCleanApiUrl(ext);
  if (!baseUrl) {
    logError('API URL 未配置');
    return null;
  }
  const apiUrl = needBase64
    ? `${baseUrl}/api/v1/character/random?image_format=base64`
    : `${baseUrl}/api/v1/character/random`;
  logDebug(ext, `请求API: ${apiUrl}`);

  const response = await fetchWithRetry(ext, apiUrl);
  if (!response) {
    logError('API 请求最终失败');
    return null;
  }

  try {
    return (await response.json()) as CharacterData;
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : String(e);
    logDebug(ext, `JSON解析失败: ${message}`);
    return null;
  }
}

export async function getStatus(ext: seal.ExtInfo): Promise<StatusResponse | null> {
  const baseUrl = getCleanApiUrl(ext);
  if (!baseUrl) return null;
  const apiUrl = `${baseUrl}/api/v1/status`;
  const response = await fetchWithRetry(ext, apiUrl);
  if (!response) return null;

  try {
    return (await response.json()) as StatusResponse;
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : String(e);
    logDebug(ext, `Status JSON解析失败: ${message}`);
    return null;
  }
}
