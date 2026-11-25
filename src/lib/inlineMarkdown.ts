import { localizePath, type Locale } from '../i18n/routing.ts';

export const VERIFIED_MODULE_TARGETS: Record<string, string[]> = {
  'lsposed': ['LSPosed Framework', 'LSPosed', 'Xposed Framework', 'Xposed runtime', 'EdXposed'],
  'shizuku': ['Shizuku service', 'Shizuku'],
  'dhizuku': ['Dhizuku'],
  'playintegrityfix': ['Play Integrity Fix', 'PlayIntegrityFix', 'PIF'],
  'playintegrityfork': ['Play Integrity Fork', 'PlayIntegrityFork'],
  'trickystore': ['TrickyStore', 'Tricky Store', 'Tricky_Store'],
  'trickystoreoss': ['TrickyStoreOSS', 'Tricky Store OSS'],
  'teesimulator': ['TEESimulator', 'TEE Simulator'],
  'teesimulator-rs': ['TEESimulator-RS', 'TEE Simulator RS'],
  'shamiko': ['Shamiko'],
  'zygisknext': ['ZygiskNext', 'Zygisk Next', 'Zygisk-Next'],
  'rezygisk': ['ReZygisk'],
  'neozygisk': ['NeoZygisk'],
  'onyxzygisk': ['OnyxZygisk'],
  'vexzygisk': ['VexZygisk'],
  'zygisk-assistant': ['Zygisk Assistant', 'Zygisk-Assistant'],
  'bindhosts': ['bindhosts', 'Systemless hosts'],
  'acc': ['Advanced Charging Controller', 'ACC'],
  'miui-theme-rights-enabler': ['Apk Protection Patch', 'Theme Rights Enabler', 'MIUI Theme Rights', 'Core Patch'],
  'viper4android-dolby-coexistence': ['ViPER4Android & Dolby Atmos Coexistence', 'ViPER4Android', 'Viper4Android'],
  'viperfx-re': ['ViPERFX_RE', 'ViPERFX-RE'],
  'dsp-audiofix': ['DSP Audio Fix', 'dsp-audiofix'],
  'leica-camera-port': ['Leica Camera', 'Leica camera'],
  'miui-gallery-feature-unlocker': ['MIUI Gallery Feature Unlocker', 'Gallery AI feature', 'Gallery AI'],
  'app-manager': ['App Manager'],
  'canta': ['Canta'],
  'hail': ['Hail'],
  'adguardhomeforroot': ['AdGuard Home for Root', 'AdGuardHome'],
  'freepps-xiaomi-fast-charge': ['FreePPS', 'FreePPS Xiaomi'],
  'battery-health-query': ['Battery Health Query'],
  'quantitative-charge-cutoff': ['Quantitative Charge Cutoff', 'BH Quantitative Charging Cutoff'],
  'movecertificate': ['MoveCertificate'],
  'alwaystrustusercerts': ['AlwaysTrustUserCerts'],
  'drc-remover': ['drc-remover'],
  'usb-samplerate-unlocker': ['usb-samplerate-unlocker'],
  'yetanotherbootloopprotector': ['YetAnotherBootloopProtector'],
  'ashlooper': ['AshLooper', 'AshReXcue'],
  'knoxpatch': ['KnoxPatch'],
  'ohmykeymint': ['OhMyKeymint'],
  'stealthdebug': ['StealthDebug'],
  'magicalprotection': ['MagicalProtection'],
  'sui': ['Sui'],
  'alwaysstrong': ['AlwaysStrong'],
  'yurikey': ['YuriKey'],
  'specter': ['Specter'],
  'playcurlnext': ['playcurlNEXT', 'playcurlnext'],
  'tricky-addon-update-target-list': ['Tricky Addon', 'tricky-addon-update-target-list'],
  'nohello': ['NoHello'],
  'makefontsgreatagain': ['MakeFontsGreatAgain'],
  'material-files': ['Material Files'],
  'install-with-options': ['Install with Options'],
  'vpnhide': ['vpnhide', 'VpnHide'],
  'librepods': ['librepods', 'LibrePods'],
  'locusmimic': ['LocusMimic'],
  'lspdoze': ['LSPDoze'],
  'qishui-music-svip-unlocker': ['Soda Music SVIP', 'Qishui Music SVIP', 'qishui-music-svip-unlocker'],
  'treat-wheel-zygisk': ['Treat-Wheel-Zygisk'],
  'iunlockergl': ['iUnlockerGL'],
  'magisk-ad-blocking-module': ['Magisk-Ad-Blocking-Module'],
  'meta-magic-mount-rs': ['Magic Mount-rs', 'meta-magic_mount-rs', 'meta-magic-mount-rs'],
  'magisk-frida': ['MagiskFrida', 'magisk-frida'],
  'copg-vd': ['COPG-VD'],
  'corepatch': ['CorePatch', 'Core Patch'],
  'disable-flag-secure': ['DisableFlagSecure', 'Disable FLAG_SECURE', 'Enable Screenshot'],
  'waenhancer': ['WaEnhancer'],
  'installerx-revived': ['InstallerX Revived', 'InstallerX-Revived', 'InstallerX'],
  'pixelxpert-next': ['PixelXpert-Next', 'PixelXpert'],
  'tricky-addon-enhanced': ['Tricky Addon Enhanced', 'TA_enhanced'],
  'unlock-cn-gms': ['Unlock CN GMS', 'unlock-cn-gms'],
  'reqable': ['Reqable'],
  'mesa-turnip-builder': ['Mesa Turnip', 'Freedreno Turnip', 'Turnip Vulkan'],
  'fde-ai': ['FDE.AI', 'FeraDroid Engine'],
  'nsg-tweaks': ['NSG Tweaks'],
  'busybox-ndk': ['BusyBox NDK', 'Busybox for Android NDK', 'busybox-ndk'],
  'camera2api-hal3-mtk': ['Camera2API HAL3', 'Camera2 API MTK'],
  'joyctl-android': ['JoyCtl Android', 'JoyCtl'],
  'blurclosed': ['Blur Closed', 'BlurClosed'],
};

export function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** Escape raw text first, then render inline code spans and bold spans safely. */
export function parseInlineMarkdown(text: string): string {
  if (!text) return '';
  const escaped = escapeHtml(text);
  const codeTokens: string[] = [];
  const withCodePlaceholders = escaped.replace(/`([^`]+)`/g, (_m, codeInner) => {
    const token = `\u0000CODE${codeTokens.length}\u0000`;
    codeTokens.push(
      `<code class="bg-zinc-100 text-zinc-800 border border-zinc-200 text-xs font-mono px-1.5 py-0.5 rounded">${codeInner}</code>`
    );
    return token;
  });
  const withBold = withCodePlaceholders.replace(/\*\*([^*\n]+)\*\*/g, '<strong class="font-semibold text-zinc-900">$1</strong>');
  return withBold.replace(/\u0000CODE(\d+)\u0000/g, (_m, idx) => codeTokens[Number(idx)] ?? '');
}

/** Render inline markdown while adding verified cross-links only inside plain text nodes (never inside <a> or <code>). */
export function renderEntityMarkdown(
  text: string,
  currentSlug: string,
  locale: Locale = 'en',
  isConflict: boolean = false
): string {
  if (!text) return '';
  let html = parseInlineMarkdown(text);

  for (const [targetSlug, aliases] of Object.entries(VERIFIED_MODULE_TARGETS)) {
    if (targetSlug === currentSlug) continue;
    for (const alias of aliases) {
      const regex = new RegExp(`\\b(${escapeRegExp(alias)})\\b`, 'i');
      const parts = html.split(/(<a\b[^>]*>.*?<\/a>|<code\b[^>]*>.*?<\/code>|<[^>]+>)/gi);
      let matched = false;
      html = parts
        .map((part) => {
          if (part.startsWith('<') || matched) return part;
          if (regex.test(part)) {
            matched = true;
            const linkClass = isConflict
              ? 'font-medium text-rose-700 underline underline-offset-2 hover:text-rose-900 transition-colors'
              : 'font-medium text-zinc-900 underline underline-offset-2 hover:text-black transition-colors';
            const targetHref = localizePath(`/modules/${targetSlug}/`, locale);
            return part.replace(regex, `<a href="${targetHref}" class="${linkClass}">$1</a>`);
          }
          return part;
        })
        .join('');
      if (matched) break;
    }
  }
  return html;
}
