from spacy.language import Language
from spacy.tokens import Span

@Language.component("merge_spans")
def merge_spans(doc):
    # Assuming "spans" is an attribute in the doc's custom extensions
    # Make sure to create this attribute before calling this component
    original_spans = list(doc.spans["main"])
    
    # We will merge spans that overlap and have the same label
    merged_spans = []
    original_spans.sort(key=lambda x: x.start) # Sort by start index
    
    # Iterate through the sorted spans
    for span in original_spans:
        if merged_spans and span.start <= merged_spans[-1].end and span.label_ == merged_spans[-1].label_:
            # If the current span overlaps with the last merged span and has the same label, extend the last merged span
            merged_spans[-1] = Span(doc, merged_spans[-1].start, max(span.end, merged_spans[-1].end), label=span.label_)
        else:
            # Otherwise, add the current span to the merged spans
            merged_spans.append(span)
    
    # Replace the original spans with the merged spans
    doc.spans["main"] = merged_spans
    
    return doc


@Language.component("find_relations")
def find_relations(doc):
    for span in doc.spans["main"]:
        if len(doc) != span.end:
            if doc[span.end].text.lower() in ["son", "daughter"] and doc[span.end+1].text == "of":
                for span2 in doc.spans["main"]:
                    if span2.start == span.end+2:
                        doc.spans["main"].append(Span(doc, span.start, span2.end, label="RELATION"))
    return doc