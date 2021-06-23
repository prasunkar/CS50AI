
# 🧐 Parser Project

**Objective:** Write an AI to parse sentences and extract noun phrases.

## 📺 Demonstration

```
$ python parser.py
Sentence: Holmes sat.
        S
   _____|___
  NP        VP
  |         |
  N         V
  |         |
holmes     sat

Noun Phrase Chunks
holmes
```

## 🌉 Background

A common task in natural language processing is parsing, the process of determining the structure of a sentence. This is useful for a number of reasons: knowing the structure of a sentence can help a computer to better understand the meaning of the sentence, and it can also help the computer extract information out of a sentence. In particular, it’s often useful to extract noun phrases out of a sentence to get an understanding for what the sentence is about.

In this problem, we’ll use the context-free grammar formalism to parse English sentences to determine their structure. Recall that in a context-free grammar, we repeatedly apply rewriting rules to transform symbols into other symbols. The objective is to start with a nonterminal symbol  `S`(representing a sentence) and repeatedly apply context-free grammar rules until we generate a complete sentence of terminal symbols (i.e., words). The rule  `S -> N V`, for example, means that the  `S`  symbol can be rewritten as  `N V`  (a noun followed by a verb). If we also have the rule  `N -> "Holmes"`  and the rule  `V -> "sat"`, we can generate the complete sentence  `"Holmes sat."`.

Of course, noun phrases might not always be as simple as a single word like  `"Holmes"`. We might have noun phrases like  `"my companion"`  or  `"a country walk"`  or  `"the day before Thursday"`, which require more complex rules to account for. To account for the phrase  `"my companion"`, for example, we might imagine a rule like:

```
NP -> N | Det N
```

In this rule, we say that an  `NP`  (a “noun phrase”) could be either just a noun (`N`) or a determiner (`Det`) followed by a noun, where determiners include words like  `"a"`,  `"the"`, and  `"my"`. The vertical bar (`|`) just indicates that there are multiple possible ways to rewrite an  `NP`, with each possible rewrite separated by a bar.

To incorporate this rule into how we parse a sentence (`S`), we’ll also need to modify our  `S -> N V`  rule to allow for noun phrases (`NP`s) as the subject of our sentence. See how? And to account for more complex types of noun phrases, we may need to modify our grammar even further.

## 🧐 Understanding

First, look at the text files in the  `sentences`  directory. Each file contains an English sentence. The goal in this problem is to write a parser that is able to parse all of these sentences.

Take a look now at  `parser.py`, and notice the context free grammar rules defined at the top of the file. I have already defined a set of rules for generating terminal symbols (in the global variable  `TERMINALS`). Notice that  `Adj`  is a nonterminal symbol that generates adjectives,  `Adv`  generates adverbs,  `Conj`  generates conjunctions,  `Det`generates determiners,  `N`  generates nouns (spread across multiple lines for readability),  `P`  generates prepositions, and  `V`  generates verbs.

Next is the definition of  `NONTERMINALS`, which will contain all of the context-free grammar rules for generating nonterminal symbols. Right now, there’s just a single rule:  `S -> N V`. With just that rule, we can generate sentences like  `"Holmes arrived."`  or  `"He chuckled."`, but not sentences more complex than that.

Next, take a look at the  `main`  function. It first accepts a sentence as input, either from a file or via user input. The sentence is preprocessed (via the  `preprocess`  function) and then parsed according to the context-free grammar defined by the file. The resulting trees are printed out, and all of the “noun phrase chunks” (defined in the Specification) are printed as well (via the  `np_chunk`  function).
