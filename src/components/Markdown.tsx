import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { Children, isValidElement, type ReactElement, type ReactNode } from "react";
import type { Lang } from "../content";

const LABEL: Record<string, string> = { java: "Java", python: "Python", javascript: "JavaScript", js: "JavaScript" };
const LANG_OF: Record<string, Lang> = { java: "java", python: "python", javascript: "javascript", js: "javascript" };

function text(node: ReactNode): string {
  return Children.toArray(node)
    .map((c) => (typeof c === "string" ? c : isValidElement(c) ? text((c.props as { children?: ReactNode }).children) : ""))
    .join("");
}

export function slug(s: string) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

/**
 * Keeps `:::only java` / `:::only python,javascript` regions that apply to `lang`
 * and drops the marker lines. Blocks do not nest: a `:::` line closes only an open block.
 * With no `lang`, every region is kept and the markers are still removed.
 */
export function filterForLang(text: string, lang?: Lang): string {
  const lines = text.split("\n");
  const out: string[] = [];
  let allowed: Set<string> | null = null;
  for (const line of lines) {
    const trimmed = line.trim();
    if (allowed === null) {
      const opened = /^:::only\s+(.+)$/.exec(trimmed);
      if (opened) {
        allowed = new Set(
          opened[1]
            .split(",")
            .map((s) => s.trim().toLowerCase())
            .filter(Boolean),
        );
        continue;
      }
      out.push(line);
      continue;
    }
    if (trimmed === ":::") {
      allowed = null;
      continue;
    }
    if (!lang || allowed.has(lang)) out.push(line);
  }
  return out.join("\n");
}

/**
 * Renders guide/statement markdown. Code blocks tagged java / python / javascript
 * are shown only for the learner's chosen language. `:::only` regions are filtered first.
 */
export function Markdown({ text: src, lang }: { text: string; lang?: Lang }) {
  const body = filterForLang(src, lang);
  return (
    <div className="prose">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[[rehypeHighlight, { detect: false }]]}
        components={{
          h2({ children }) {
            return <h2 id={slug(text(children))}>{children}</h2>;
          },
          pre({ children, ...rest }) {
            const child = (Array.isArray(children) ? children[0] : children) as ReactElement<{ className?: string }>;
            const m = /language-(\w+)/.exec(child?.props?.className ?? "");
            const blockLang = m?.[1];
            if (lang && blockLang && LANG_OF[blockLang] && LANG_OF[blockLang] !== lang) return null;
            const { node: _node, ...props } = rest as typeof rest & { node?: unknown };
            return (
              <pre {...props} data-lang={blockLang ? LABEL[blockLang] : undefined}>
                {children}
              </pre>
            );
          },
          a({ href, children }) {
            return (
              <a href={href} target="_blank" rel="noreferrer">
                {children}
              </a>
            );
          },
        }}
      >
        {body}
      </ReactMarkdown>
    </div>
  );
}
