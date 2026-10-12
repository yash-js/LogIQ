// Detects ready-made library helpers ("shortcuts") in the learner's code.
// Using them is allowed, but the problem then offers a Pure challenge:
// solve it again with plain loops and conditions for bonus XP.

import type { Lang, Problem } from "../content";

export interface Shortcut {
  id: string;
  label: string;
  tip: string;
  found: string;
}

interface Rule {
  id: string;
  label: string;
  tip: string;
  patterns: Partial<Record<Lang, RegExp>>;
  /** Skip this rule for some problems (e.g. BigInt is required for huge answers in JS). */
  skip?: (p: Problem) => boolean;
  /** Only apply to these problem ids. */
  only?: string[];
}

const RULES: Rule[] = [
  {
    id: "sort",
    label: "sorting",
    tip: "Sort with your own loops (selection or bubble sort), or find a way that doesn't need sorting at all.",
    patterns: {
      java: /\b(?:Arrays|Collections)\s*\.\s*sort\b|\.sort\s*\(|\.sorted\s*\(/,
      python: /\bsorted\s*\(|\.sort\s*\(/,
      javascript: /\.(?:sort|toSorted)\s*\(/,
    },
  },
  {
    id: "set",
    label: "Set",
    tip: "Use a boolean array (for example boolean[26] for letters) or compare with nested loops.",
    patterns: {
      java: /\b(?:Hash|Tree|LinkedHash)?Set\s*</ ,
      python: /\b(?:set|frozenset)\s*\(/,
      javascript: /\bnew\s+(?:Weak)?Set\b/,
    },
  },
  {
    id: "map",
    label: "Map / dictionary",
    tip: "Keep counts in an int array indexed by the value or character code.",
    patterns: {
      java: /\b(?:Hash|Tree|LinkedHash)?Map\s*</,
      python: /\b(?:dict|Counter|defaultdict|OrderedDict)\s*\(|\bcollections\b|\{\s*\}/,
      javascript: /\bnew\s+(?:Weak)?Map\b|\bObject\s*\.\s*(?:keys|values|entries)\b/,
    },
  },
  {
    id: "maxmin",
    label: "max / min helpers",
    tip: "Compare with if-statements and keep the best value in a variable.",
    patterns: {
      java: /\bMath\s*\.\s*(?:max|min)\b|Collections\s*\.\s*(?:max|min)\b/,
      python: /\b(?:max|min)\s*\(/,
      javascript: /\bMath\s*\.\s*(?:max|min)\b/,
    },
  },
  {
    id: "reverse",
    label: "reverse helpers",
    tip: "Reverse with two pointers, or build the result from the end.",
    patterns: {
      java: /\.reverse\s*\(|Collections\s*\.\s*reverse\b/,
      python: /\[\s*:\s*:\s*-\s*1\s*\]|\breversed\s*\(|\.reverse\s*\(/,
      javascript: /\.(?:reverse|toReversed)\s*\(/,
    },
  },
  {
    id: "power",
    label: "power / square root",
    tip: "Multiply in a loop (or write your own fast power) instead.",
    patterns: {
      java: /\bMath\s*\.\s*(?:pow|sqrt|cbrt|hypot)\b/,
      python: /\bmath\s*\.\s*(?:pow|sqrt|isqrt|factorial|gcd|lcm|comb|perm)\b|\bpow\s*\(|\*\*/,
      javascript: /\bMath\s*\.\s*(?:pow|sqrt|cbrt|hypot)\b|\*\*/,
    },
  },
  {
    id: "aggregate",
    label: "sum / streams / reduce",
    tip: "Add things up with a plain loop and an accumulator variable.",
    patterns: {
      java: /\.stream\s*\(|\bArrays\s*\.\s*stream\b|\b(?:Int|Long)Stream\b/,
      python: /\bsum\s*\(|\b(?:any|all)\s*\(|\bfunctools\b|\breduce\s*\(/,
      javascript: /\.(?:reduce|reduceRight|some|every)\s*\(/,
    },
  },
  {
    id: "base",
    label: "built-in number conversion",
    tip: "Convert between bases with % and / in a loop.",
    patterns: {
      java: /\b(?:Integer|Long)\s*\.\s*(?:toBinaryString|toOctalString|toHexString|bitCount|highestOneBit|numberOfLeadingZeros)\b|\b(?:Integer|Long)\s*\.\s*(?:toString|parseInt|parseLong|valueOf)\s*\([^()]*,[^()]*\)/,
      python: /\b(?:bin|oct|hex)\s*\(|\bint\s*\([^()]*,\s*\d+\s*\)|\.bit_(?:count|length)\s*\(/,
      javascript: /\.toString\s*\(\s*\d+\s*\)|\bparseInt\s*\([^()]*,\s*\d+\s*\)/,
    },
  },
  {
    id: "bignum",
    label: "big-number types",
    tip: "Do the arithmetic digit by digit, carrying like on paper.",
    patterns: { java: /\bBig(?:Integer|Decimal)\b/, javascript: /\bBigInt\b|\d+n\b/ },
    skip: (p) => p.returns === "long" || p.returns === "long_list",
  },
  {
    id: "wholeint",
    label: "converting the whole number string",
    tip: "These numbers can be thousands of digits long. Add or multiply digit by digit instead.",
    patterns: {
      python: /\bint\s*\(\s*(?:(?:num1|num2|a|b)\s*[,)]|["']{2}\s*\.\s*join)/,
      java: /\b(?:Integer|Long)\s*\.\s*(?:parseInt|parseLong|valueOf)\s*\(\s*(?:num1|num2|a|b)\s*\)/,
      javascript: /\b(?:Number|parseInt|parseFloat)\s*\(\s*(?:num1|num2|a|b)\s*[,)]/,
    },
    only: ["p5-20", "p6-06", "p6-07", "p6-23"],
  },
  {
    id: "count",
    label: ".count()",
    tip: "Count with a loop and a counter variable.",
    patterns: { python: /\.count\s*\(/ },
  },
  {
    id: "search",
    label: "string / list search",
    tip: "Compare element by element in a loop.",
    patterns: {
      java: /\.(?:indexOf|lastIndexOf|contains|startsWith|endsWith|matches)\s*\(/,
      python: /\.(?:find|rfind|index|rindex|startswith|endswith)\s*\(/,
      javascript: /\.(?:indexOf|lastIndexOf|includes|startsWith|endsWith|search|match|matchAll|find|findIndex|findLast)\s*\(/,
    },
  },
  {
    id: "case",
    label: "case / character-class helpers",
    tip: "Use character codes: 'A'..'Z' and 'a'..'z' are consecutive ranges, 32 apart.",
    patterns: {
      java: /\.(?:toLowerCase|toUpperCase)\s*\(|\bCharacter\s*\.\s*(?:is\w+|to(?:Lower|Upper)Case)\b/,
      python: /\.(?:lower|upper|isdigit|isalpha|isalnum|isupper|islower|isnumeric|isdecimal|swapcase|capitalize|title|casefold)\s*\(/,
      javascript: /\.(?:toLowerCase|toUpperCase|toLocaleLowerCase|toLocaleUpperCase)\s*\(/,
    },
  },
  {
    id: "strops",
    label: "replace / split / trim",
    tip: "Walk the string with an index and build the result yourself.",
    patterns: {
      java: /\.(?:replace|replaceAll|replaceFirst|split|trim|strip|stripLeading|stripTrailing)\s*\(/,
      python: /\.(?:replace|split|rsplit|splitlines|strip|lstrip|rstrip|partition)\s*\(/,
      javascript: /\.(?:replace|replaceAll|split|trim|trimStart|trimEnd|padStart|padEnd)\s*\(/,
    },
  },
  {
    id: "regex",
    label: "regular expressions",
    tip: "Check each character with conditions instead of a pattern.",
    patterns: { java: /\bPattern\s*\.\s*compile\b/, python: /\bimport\s+re\b|\bre\s*\.\s*\w+\s*\(/, javascript: /\bnew\s+RegExp\b|\.test\s*\(/ },
  },
  {
    id: "dates",
    label: "date libraries",
    tip: "Count days yourself: years, then months, then days.",
    patterns: {
      java: /\bjava\s*\.\s*time\b|\bLocalDate\b|\bCalendar\b|\bDayOfWeek\b/,
      python: /\b(?:datetime|calendar)\b/,
      javascript: /\bnew\s+Date\b|\bDate\s*\./,
    },
  },
];

/** Removes comments and string/char literals so they can't trigger rules. */
function stripNoise(code: string, lang: Lang): string {
  if (lang === "python") {
    return code
      .replace(/("""|''')[\s\S]*?\1/g, '""')
      .replace(/(["'])(?:\\.|(?!\1)[^\\\n])*\1/g, '""')
      .replace(/#.*$/gm, "");
  }
  return code
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/`(?:\\.|[^\\`])*`/g, '""')
    .replace(/(["'])(?:\\.|(?!\1)[^\\\n])*\1/g, '""')
    .replace(/\/\/.*$/gm, "");
}

const MARKER = "input / output is handled below";

/** The part of the file the learner writes: everything above the I/O marker. */
export function learnerRegion(code: string): string {
  const i = code.indexOf(MARKER);
  if (i < 0) return code;
  const lineStart = code.lastIndexOf("\n", i);
  return code.slice(0, lineStart < 0 ? 0 : lineStart);
}

export function findShortcuts(code: string, lang: Lang, problem: Problem): Shortcut[] {
  const src = stripNoise(learnerRegion(code), lang);
  const out: Shortcut[] = [];
  for (const r of RULES) {
    if (r.only && !r.only.includes(problem.id)) continue;
    if (r.skip?.(problem)) continue;
    const re = r.patterns[lang];
    if (!re) continue;
    const m = re.exec(src);
    if (m) out.push({ id: r.id, label: r.label, tip: r.tip, found: m[0].trim() });
  }
  return out;
}
