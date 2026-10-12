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
 * Renders guide/statement markdown. Code blocks tagged java / python / javascript
 * are shown only for the learner's chosen language.
 */
export function Markdown({ text: src, lang }: { text: string; lang?: Lang }) {
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
        {src}
      </ReactMarkdown>
    </div>
  );
}
