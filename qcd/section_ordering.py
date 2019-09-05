import itertools
import statistics

import plac

from qcd.concept_graph import ConceptGraph
from qcd.xml_parser import XMLParser


@plac.annotations(
    file=plac.Annotation("The file to parse. Must be a XML formatted file.", type=str),
    disable_implicit_references=plac.Annotation('Flag indicating to not add implicit references.', kind='flag',
                                                abbrev='i'),
    disable_reference_marking=plac.Annotation('Flag indicating to not mark reference types.', kind='flag', abbrev='m'),
    disable_edge_annotation=plac.Annotation('Flag indicating to not annotate edges with relation types.', kind='flag',
                                            abbrev='a'),
    disable_summary=plac.Annotation('Flag indicating to not print the graph summary.', kind='flag', abbrev='s'),
    disable_graph_rendering=plac.Annotation('Flag indicating to not render (visualise) the graph structure.',
                                            kind='flag',
                                            abbrev='r')

)
def main(file, disable_implicit_references=False, disable_reference_marking=False, disable_edge_annotation=False,
         disable_summary=False, disable_graph_rendering=False):
    """Run an experiment testing how ordering of sections affects the scoring of conceptual density for a given
    document.
    """

    graph = ConceptGraph(parser=XMLParser(not disable_edge_annotation, not disable_implicit_references),
                         mark_references=not disable_reference_marking)
    graph.parse(file)

    if not disable_summary:
        graph.print_summary()

    print('Original Section Ordering: %s' % graph.sections)
    print('Score on Original Ordering: %.2f' % graph.score())

    if not disable_graph_rendering:
        graph.render()

    scores = []
    permutations = []

    for permutation in itertools.permutations(graph.sections):
        scores.append(graph.score())
        permutations.append(permutation)
        graph.sections = permutation
        graph.postprocessing()

    min_score = min(scores)
    max_score = max(scores)

    print('scores: %s' % ['%.2f' % score for score in scores])
    print('min: %.2f - ordering: %s' % (min_score, permutations[scores.index(min_score)]))
    print('max: %.2f - ordering: %s' % (max_score, permutations[scores.index(max_score)]))
    print('Mean: %.2f - Std. Dev.: %.2f' % (sum(scores) / len(scores), statistics.stdev(scores)))
    print('Max Absolute Difference: %.2f - Max Diff. Ratio: %.2f' % (max_score - min_score,
                                                                     (max_score - min_score) / max_score))


if __name__ == '__main__':
    plac.call(main)