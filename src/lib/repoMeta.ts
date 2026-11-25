const REPO_API_URL = 'https://api.github.com/repos/Yass5002/magisk-hub';
const FALLBACK_STAR_COUNT = 4;

let cachedStarCountPromise: Promise<number> | null = null;

/** Fetch repository star count once per Astro static build with safe fallback. */
export function getSiteRepoStars(): Promise<number> {
  if (cachedStarCountPromise) return cachedStarCountPromise;

  cachedStarCountPromise = (async () => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 2500);
    try {
      const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
      const headers: Record<string, string> = {
        Accept: 'application/vnd.github+json',
        'User-Agent': 'MagiskHub-Builder/1.0',
      };
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
      const resp = await fetch(REPO_API_URL, { headers, signal: controller.signal });
      if (!resp.ok) return FALLBACK_STAR_COUNT;
      const data = await resp.json();
      if (typeof data?.stargazers_count === 'number' && data.stargazers_count >= 0) {
        return data.stargazers_count;
      }
    } catch {
      // Build continues cleanly offline or under API rate limits
    } finally {
      clearTimeout(timer);
    }
    return FALLBACK_STAR_COUNT;
  })();

  return cachedStarCountPromise;
}

export function formatCompactStars(count: number): string {
  if (count >= 1000) {
    return `${(count / 1000).toFixed(1).replace(/\.0$/, '')}k`;
  }
  return count.toString();
}
