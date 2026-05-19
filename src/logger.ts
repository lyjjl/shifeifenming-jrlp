import { isDebugEnabled } from './config';

export function logDebug(ext: seal.ExtInfo, info: string): void {
  if (isDebugEnabled(ext)) {
    console.log(`[jrlp-DEBUG] ${info}`);
  }
}

export function logError(message: string): void {
  console.error(`[jrlp-ERROR] ${message}`);
}
