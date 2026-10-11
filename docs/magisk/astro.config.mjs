import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from '@astrojs/tailwind';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  site: 'https://magisk.yssn.tech',
  base: '/magisk',
  outDir: '../../dist/magisk',
  output: 'static',
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
  integrations: [
    starlight({
      title: 'Magisk Documentation',
      description: 'Complete Magisk installation guides, bootloader unlocking, and troubleshooting for Android devices.',
      logo: {
        src: './src/assets/logo.png',
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/Yass5002/magisk-hub' }
      ],
      components: {
        Header: './src/components/Header.astro',
        ThemeProvider: './src/components/ThemeProvider.astro',
      },
      sidebar: [
        {
          label: 'Guide',
          items: [
            { label: 'Installation Overview', link: '/' },
            { label: 'Download Magisk', slug: 'guide/download' },
            { label: 'Switch / Update Version', slug: 'guide/switch-version' },
          ],
        },
        {
          label: 'Installation by Device',
          items: [
            { label: 'Xiaomi / Redmi (boot.img)', slug: 'install/xiaomi-boot' },
            { label: 'Xiaomi / Redmi (init_boot.img)', slug: 'install/xiaomi-init-boot' },
            { label: 'OnePlus (boot.img)', slug: 'install/oneplus-boot' },
            { label: 'OnePlus (init_boot.img)', slug: 'install/oneplus-init-boot' },
            { label: 'Realme (boot.img)', slug: 'install/realme-boot' },
            { label: 'Realme (init_boot.img)', slug: 'install/realme-init-boot' },
            { label: 'Motorola (boot.img)', slug: 'install/motorola-boot' },
            { label: 'Motorola (init_boot.img)', slug: 'install/motorola-init-boot' },
            { label: 'Google Pixel (boot.img)', slug: 'install/pixel-boot' },
            { label: 'Google Pixel (init_boot.img)', slug: 'install/pixel-init-boot' },
            { label: 'Samsung (boot.img)', slug: 'install/samsung-boot' },
            { label: 'Samsung (init_boot.img)', slug: 'install/samsung-init-boot' },
            { label: 'LightSpeed Virtual Machine', slug: 'install/virtual-machine' },
          ],
        },
        {
          label: 'Bootloader Unlocking',
          items: [
            { label: 'Xiaomi / Redmi', slug: 'unlock/xiaomi' },
            { label: 'OnePlus (Snapdragon)', slug: 'unlock/oneplus-snapdragon' },
            { label: 'OnePlus (MediaTek)', slug: 'unlock/oneplus-mediatek' },
            { label: 'OnePlus In-Depth Test App', slug: 'unlock/oneplus-app' },
            { label: 'Realme (Snapdragon)', slug: 'unlock/realme-snapdragon' },
            { label: 'Realme (MediaTek)', slug: 'unlock/realme-mediatek' },
            { label: 'Realme In-Depth Test App', slug: 'unlock/realme-app' },
            { label: 'Motorola', slug: 'unlock/motorola' },
            { label: 'Google Pixel', slug: 'unlock/pixel' },
            { label: 'Samsung', slug: 'unlock/samsung' },
          ],
        },
        {
          label: 'Boot Image Extraction & ROMs',
          items: [
            { label: 'payload-dumper-go (boot.img)', slug: 'extract/payload-dumper-boot' },
            { label: 'payload-dumper-go (init_boot.img)', slug: 'extract/payload-dumper-init-boot' },
            { label: 'Payload-Dumper-Compose Tool', slug: 'extract/payload-dumper-compose' },
            { label: 'MT Manager payload.bin Extraction', slug: 'extract/mt-manager' },
            { label: 'Download Xiaomi / MIUI ROMs', slug: 'extract/download-xiaomi-rom' },
            { label: 'Bypass Xiaomi Download Throttling', slug: 'extract/bypass-download-throttling' },
            { label: 'Frija Samsung Firmware Downloader', slug: 'extract/samsung-frija' },
            { label: 'SamFirm Samsung Firmware Downloader', slug: 'extract/samsung-samfirm' },
          ],
        },
        {
          label: 'Troubleshooting & Fixes',
          items: [
            { label: 'Fastboot: waiting for any device', slug: 'troubleshooting/waiting-for-device' },
            { label: 'Samsung USB Driver Installation', slug: 'troubleshooting/samsung-usb-driver' },
            { label: 'Samsung One UI 5 Error -45 Fix', slug: 'troubleshooting/samsung-error-45' },
            { label: 'Disable AVB Verification', slug: 'troubleshooting/disable-avb' },
            { label: 'Android 15 Post-Unlock Lock Screen Fix', slug: 'troubleshooting/android-15-lockscreen-bug' },
          ],
        },
      ],
      customCss: [
        'katex/dist/katex.min.css',
        './src/styles/theme.css',
      ],
    }),
    tailwind({ applyBaseStyles: false }),
  ],
});
