import CodeMirror from "@uiw/react-codemirror";
import { java } from "@codemirror/lang-java";
import { python } from "@codemirror/lang-python";
import { EditorView, keymap } from "@codemirror/view";
import { HighlightStyle, syntaxHighlighting, indentUnit } from "@codemirror/language";
import { tags as t } from "@lezer/highlight";
import { Prec } from "@codemirror/state";
import { useMemo } from "react";
import type { Lang } from "../content";

const theme = EditorView.theme(
  {
    "&": { backgroundColor: "#12162a", color: "#ece8df", height: "100%" },
    ".cm-content": { fontFamily: "var(--mono)", fontFeatureSettings: "\"liga\" 0, \"calt\" 0", caretColor: "#f2b544", padding: "12px 0" },
    ".cm-cursor": { borderLeftColor: "#f2b544", borderLeftWidth: "2px" },
    ".cm-gutters": { backgroundColor: "#12162a", color: "#555d7d", border: "none" },
    ".cm-activeLine": { backgroundColor: "#1a1f36" },
    ".cm-activeLineGutter": { backgroundColor: "#1a1f36", color: "#9aa0b8" },
    "&.cm-focused .cm-selectionBackground, .cm-selectionBackground, ::selection": { backgroundColor: "#34406a !important" },
    ".cm-matchingBracket": { backgroundColor: "#34406a", outline: "none" },
    ".cm-tooltip": { backgroundColor: "#1f2438", border: "1px solid #343b58" },
    ".cm-tooltip-autocomplete > ul > li[aria-selected]": { backgroundColor: "#34406a" },
  },
  { dark: true },
);

const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.modifier, t.controlKeyword], color: "#c4a7ff" },
  { tag: [t.typeName, t.className, t.standard(t.typeName)], color: "#7dd3fc" },
  { tag: [t.function(t.variableName), t.function(t.propertyName)], color: "#f2b544" },
  { tag: [t.string, t.character], color: "#86efac" },
  { tag: [t.number, t.bool, t.null], color: "#fda4af" },
  { tag: [t.comment, t.lineComment, t.blockComment], color: "#6b7394", fontStyle: "italic" },
  { tag: [t.operator], color: "#cbd5e1" },
  { tag: [t.definition(t.variableName)], color: "#ece8df" },
]);

export function CodeEditor(props: {
  lang: Lang;
  value: string;
  fontSize: number;
  onChange(v: string): void;
  onRun(): void;
  onSubmit(): void;
}) {
  const { lang, onRun, onSubmit } = props;
  const extensions = useMemo(
    () => [
      lang === "java" ? java() : python(),
      indentUnit.of("    "),
      theme,
      syntaxHighlighting(highlight),
      EditorView.lineWrapping,
      Prec.highest(
        keymap.of([
          { key: "Mod-Enter", run: () => (onRun(), true) },
          { key: "Mod-Shift-Enter", run: () => (onSubmit(), true) },
        ]),
      ),
    ],
    [lang, onRun, onSubmit],
  );
  return (
    <CodeMirror
      value={props.value}
      onChange={props.onChange}
      extensions={extensions}
      theme="none"
      height="100%"
      style={{ fontSize: props.fontSize, height: "100%" }}
      basicSetup={{ foldGutter: false, highlightActiveLine: true, autocompletion: true, tabSize: 4 }}
    />
  );
}
