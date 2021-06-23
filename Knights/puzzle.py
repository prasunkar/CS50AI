from logic import Biconditional, And, Or, Symbol, Not, model_check

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

# We know A cannot be both, so A must be a knave.
knowledge0 = And(
    # A is a knight if (and only if) is not a knave
    Biconditional(AKnight, Not(AKnave)),
    
    # A is a knight if (and only if) A's statement is True
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# It is impossible for A to say they are both knaves, making A a knave.
# Since B said nothing and A's statement is proven False, B is a knight.
knowledge1 = And(
    # A, B are each knights if (and only if) they are each not knaves
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    
    # A is a knight if (and only if) A's statement is True
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# A's statement concludes that both A, B are either knights or knaves.
# B's statement concludes that A, B are opposites, A = knight and B = knave and vice-versa
knowledge2 = And(
    # A, B are each knights if (and only if) they are each not knaves
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
   
    # A is a knight if and only if A's statement is true
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    
    # B is a knight if and only if B's statement is true
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# It is impossible for A to say they are a knave, making B a knave. Therefore,
# B's 2nd statement is false, making C a knight, which in turn reinforces the
# fact that A is a knight.
knowledge3 = And(
    # A, B, C are each knights if (and only if) they are each not knaves
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),

    # A is a knight if (and only if) either B's 1st or C's only statement is true
    # Due to the rules of this puzzle, A must be a knight as they can't explicitly
    # say they are knaves
    Or(AKnight, AKnave),
    
    # B is a knight if (and only if) its 1st statement is true
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    
    # B is a knight if (and only if) its 2nd statement is true
    Biconditional(BKnight, CKnave),
    
    # C is a knight if (and only if) its statement is true
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    
    for puzzle, knowledge in puzzles:
        print(f"\n{puzzle}")
        for symbol in symbols:
            if model_check(knowledge, symbol):
                print(f"    {symbol}")


if __name__ == "__main__":
    main()