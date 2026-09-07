/**
 * Date-dependent wording, resolved at build time.
 *
 * The site is statically generated, so "incoming student" vs "student" is
 * decided when the site is built, not when it is viewed. A rebuild on or
 * after the start date flips the wording; no comment to remember to action.
 */

/** First day of the TUM M.Sc. (2026-10-01), in local time. */
export const TUM_START = new Date(2026, 9, 1);

/** True once the TUM programme has started. */
export function hasStartedTum(now: Date = new Date()): boolean {
  return now.valueOf() >= TUM_START.valueOf();
}

/** Picks between wording for before and on/after the TUM start date. */
export function byTumStart<T>(before: T, from: T, now: Date = new Date()): T {
  return hasStartedTum(now) ? from : before;
}
