import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import type { ReactElement } from "react";
import type { Lang } from "../content";

/**
 * Renders guide/statement markdown. Code blocks tagged java or python are shown
 * only for the learner's chosen language, so each guide reads in one language.
 */
export function Markdown({ text, lang }: { text: string; lang?: Lang }) {
  return (
    <div className="prose">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[[rehypeHighlight, { detect: false, ignoreMissing: true }]]}
        components={{
          pre({ children, ...rest }) {
            const child = (Array.isArray(children) ? children[0] : children) as ReactElement<{ className?: string }>;
            const cls = child?.props?.className ?? "";
            const m = /language-(\w+)/.exec(cls);
            const blockLang = m?.[1];
            if (lang && (blockLang === "java" || blockLang === "python") && blockLang !== lang) return null;
            const label = blockLang === "java" ? "Java" : blockLang === "python" ? "Python" : undefined;
            return (
              <pre {...rest} data-lang={label}>
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
        {text}
      </ReactMarkdown>
    </div>
  );
}
