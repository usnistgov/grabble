# Grabble is for Graphs
_A Tidier, Analysis-first Data Format for Networks_

## What is "a `grabble`"? 

The name is inspired by the R _tidyverse_'s **tibble**

> _**Gra**ph Ti**bble**_

As such, a `grabble` is meant to be a _tidy_ data structure (see REF), enabling a host of analysis and exploration _quality-of-life_
improvements for network analysts. 

> _a modern reimagining of **graph data structures**, keeping what time has proven to be effective, and throwing out what is not._

Grabble is also a highly _general_ way of storing and manipulating graphs: it is intended as a _pivot_ format, that eases the transition from all the various formats for computationally representing graphs, while also making numerical 

## What are needs of modern network analysis?

Break down into two components: 1) data structure (on-disk representation, implicit mathematical meanings, ease-of-computation, storage) and 2) tooling (workflow, library interop, ergonomics, data lifecycle concerns, etc.)



### Graph Representation Data Structures 
> _Need: explicit structural meaning, Scalability, and Interoperability_ 

Often, the representations we choose to store and share our network data in carry implied constraints, or even features, that are not intended. 
In other cases, structural meaning we _need_ to be embedded in our data is not carried directly in its representation, instead relying a great deal on external documentation, unsustainable preprocessing pipeplines, or community tradition. 

Edgelists are the quintissential example of graph data structures: 

| source | target | weight (optional)|
| --- | --- | --- | 
| node A | node B |    1|
| ... | | |
| node x | node y | z | 

Despite the inherently "directed" naming in this example, it is exactly how traditional serialization is done in libraries like NetworkX of _undirected_ and directed graphs alike[^1].
This kind of implied structure is very common, whether in the use of assumed-symmetric adjacency matrices for undirected graphs (and their Laplacians). Because the underlying intention for the graph structure is missing from the data structure, documentation, unit tests, or analyst memory is required to ensure the data is being used or transformed correctly downstream.

(need a table of structural assumptions vs format here, try ref [paper](https://intranet.icar.cnr.it/wp-content/uploads/2018/12/RT-ICAR-PA-2018-06.pdf). Each has an easier or harder time directly storing each kind of graph structure, relying on postprocessing or analyst discipline)

- Edge Lists
    - basic csv's. Implicit nodes, or separate table
    - jsongraphschema
    - [Property Graph Serialization (JSON-PG)](https://arxiv.org/pdf/1907.03936.pdf) 
    - DeepGraph Multiblex/layer network
    - RDF (right? SVO triples are just... edgelists)
- key-value
    - aka Dict-of-Dict(of-dict) formats
    - gml
    - networkx
    - Traditional LPGs/GraphDBs
- matrix representation
    - adjacency
    - incidence
    - sparse (coo, csr, dok, etc.) vs dense
    - lots of conventions (-1 vs 1, weights implied)
    - Annotated Hypergraphs
    - RedisGraph (Via GraphBLAS)

> A new format should be flexible enough to define many inherent graph structural features _directly_ (weighting, directedness, node/edge properties, constraints), without relying on external metadata, documentation, or analyst tradition. 

On the other hand, there are often times where knowing an appropriate graph-like structure in the first place is an issue. 
For example, a directed graph structure is used by default when a symmentric undirected matrix would simplify analysis and better represent a real system. 
Or, perhaps a weighted graph allows for real-valued properties to be assessed, when epistemic uncertainty really only allows for boolean-valued edges. 
In (my paper REF), observational sampling leads to treating data generated via diffusion processes on an underlying graph _as the graph itself_[^2]. 
Often[^3] there is insufficient thought put into whether a hypergraph is actually needed when a _simplicial complex_ or even simple graph would do, and in other cases a graph fundamentally lacks the expressivity to model relational structures that would need hypergraphs instead. 
Rather than immediately asking questions of users like 
- what are the **weights** of each edge"? 
- what **two nodes** define this edge?
- What **order** are the two nodes for this edge in?

It is preferable to make the process of realizing a serialized data set one that naturally answers fundamental question about the nature of the structure being preserved.  

> by making key features of the data structure's format more _explicit_ and _available_, a well-designed format will naturally assist users in selecting appropriate graph structures 


[^1]: `networkx.to_pandas_edgelist(G)`
[^2]: This is incredibly common in literature. Co-occurrence networks (citations, document-term, keywords, etc.) for instance are typically generated from observational data, but those observations arose from generative, diffusive processes on underlying networks (which researchers like working together, syntactic and semantic relationships, contextual relatedness, etc.)
[^3]: [The Why, How, and When ofRepresentations for Complex Systems](https://epubs.siam.org/doi/epdf/10.1137/20M1355896)


### Tooling (todos)
libraries and what they bring to the table (and what they lack)

- networkx
- graph-tool
- use of tables/dataframes
    - tidy-graph (R and beautiful)
    - deepgraph
    - so annoying to lose node/edge metadata when round-tripping or doing aggregational stuff
- aside on vizualization (hierarchical, etc.)
- Linear Algebra
    - Sparse Graph (poorly supported scipy)
    - use in deep learning via message passing (geometric, pytrees)
    - use in riemannian optimization (graph manifold)
    - GraphBLAS (mostly a database trick, poor ML support)

The reality is that almost all of these don't interop in many meaningful ways, outside of occaisional import/export[^4]. Some attempts to deal with this are working more as parsers (in python), e.g. MetaGraph. 

On the other hand,  progress is made in _general_ toward desirable features (see AnnData, Muon, etc. )

> What does Grabble do to Address Data Structure & Tooling? 
> - Data Structure: 
>    - Labeled Incidence (role) Tensors, 
>    - unification of nodes/edges as entities,
>    - natural, extensible representations in both json and hdfs. 
> - Tooling: 
>    - sparse matrices and metadata tables coexisting in harmony as _tidy data_
>    - syncronized indices to consistently access/manipulate accross observations 
>    - typed serialization/parsing to semantic web standards and scientific data storage.
>    - easy extensibility to define custom node/edge behavior and data  


[^4]: See Michael Coscia's [lovely diatribe](https://arxiv.org/pdf/2101.00863.pdf#chapter.46) in his WIP textbook, _Atlas for the Aspiring Network Scientist_

### Incidence Structures

### "Roles"

### HDF

# What is Grabble? 


## Standard Data Format 
- schema spec
- variety of graph types
- HDF with sparse data

## Python Library
- validation
- easy manipulation built on AnnData
- custom algorithms
- foundation for Nestor (v1.0+)

# More Reading

## Reading Material
papers I would like to use as tone/template guides 
- [Muon: multimodal omics analysis framework](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02577-8) (I want to write the grabble paper very much like this one, and in fact the data structure is very similar, but omics-focused):
- RedisGraph and Matrix-based Graph Algorithms; [GraphBLAS foundations paper](https://arxiv.org/pdf/1606.05790.pdf) (incidence matrix as the foundational unit came from this )
- [Annotated Hypergraphs](https://arxiv.org/pdf/1911.01331.pdf) (how to separate edges from their nodes... roles!)
- [DeepGraph](https://arxiv.org/pdf/1604.00971.pdf)  ( view every thing as possible entity sets that we can connect to others with ~~edges~~ incidences... edges _are_ entities)
- [algebraic graphs with class](https://dl.acm.org/doi/pdf/10.1145/3122955.3122956)  ( really good, deep thoughts on user workflow and structure as _helping_ that)
- graphs vs. Simplicial Complexes Vs. Hypergraphs ... [The Why, How, and When ofRepresentations for Complex Systems](https://epubs.siam.org/doi/epdf/10.1137/20M1355896) (just a great paper)

## Projects that `grabble` uses
- `anndata`
- `pandas`
- `staticframe`
- `beartype`


## Inspirational Projects
- `redisgraph`
- `loompy`
- `networkx`
- `tidy-graph`
- `tibble`
- `metagraph`
- `deepgraph`
- `TypeDB` (previously Grakn)


