import { registerCommands, registerNonCommandHandler } from './commands';
import { registerConfigs } from './config';
import { cleanExpiredMarriages } from './marriage';
import { initStorage } from './storage';

function main(): void {
  let ext = seal.ext.find('今日老婆');
  if (!ext) {
    ext = seal.ext.new('今日老婆', '群友，艾因，是非', '1.3.0');
    seal.ext.register(ext);

    registerConfigs(ext);
    initStorage(ext);
    registerCommands(ext);
    registerNonCommandHandler(ext);

    seal.ext.registerTask(
      ext,
      'daily',
      '0:00',
      () => {
        cleanExpiredMarriages(ext);
      },
      'jrlp_marriage_check',
      '每日婚姻过期检查',
    );
  }
}

main();
