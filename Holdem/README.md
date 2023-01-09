# Game Rules

Holdem is a simulation of tournament style Texas Hold 'em. Holdem will continue until there is only one player
remaining with money. Each Player will begin with a thousand dollars. The players continue to play hands until they
run out of money or are the last player standing.


## Equipment:

Holdem is played with a traditional 52 card deck. This deck contains ace through king in the four different suits. These
suits are hearts, diamonds, spades, and clubs. The initial configuration will consist of each player having two cards and there being five cards on the board. Initially, only three of the five cards will be faced up on the board.

Here is an example of how the initial configuration of the board looks:

![Example of the Board](/resources/defaultBoardSetup.png)

## Game Flow

- Initially, each player is dealt a card from the shuffled deck in the current player order. Once each person has one card, each player is 
dealt another card in the same order. 

- Once all players have two cards, the players will each place an ante of 50 dollars. 

- After the antes are placed into the pot, the five card board will begin to be built. The dealer places the first three cards dealt to the board face up. The next two are faced down until later in the hand. 

- Once these first three cards are placed face up, the first round of betting will begin. The betting will go in the current player order. 

- The players have three options. They can either bet 50 dollars, fold, or check. One of these options will be picked depending on the player's opinion on the strength of their hand. There will be a hierarchy of the strength of hands listed later in this read me. 

    To bet means that the player believes they have a strong hand, so they want the other players to increase the amount of money in the pot by matching his or her bet to continue playing. 

    To fold the hand means that the player no longer wants to play their hand because it is weak. They will give up their cards and sit out for the rest of the hand. 

    To check means that the player does not want to bet or fold. A player may only check if no bet has been placed by a player before them. If someone has bet before them they must match the bet to continue playing, otherwise, they must fold.

- To make this concept more clear, I will describe an example: consider if we have players A, B, C, and D and the betting goes in that order. The round of betting will begin with player A. Say that player A decides to check. After A checks, it is now B's turn. Say that B decides to bet 50 dollars. It is now C's turn. C decides to fold, so he will sit out for the rest of the hand. It is now D's turn. D decides he wants to play so he also puts 50 more dollars in the pot. 

- Once the first round of betting is complete, the fourth card is revealed. Another round of betting in the same fashion will then be carried out in the same order.  

- Upon the conclusion of the final round of betting, the players still playing will reveal their cards. The player with the strongest hand will win the money in the pot. This is the conclusion of one hand. 


## Player Order:

Before each hand, the order the players is shifted by one. Players are dealt cards and bet in the same order. For example, if in the first hand we have the order A, B, C, and then D, on the next hand the order would be B, C, D, A. 


## Hand Strength Hierarchy

In this version of poker, there are 9 possible hands--listed from weakest to strongest:
1. High Card - The highest of the two cards you have. For example, you have the ace of spades. This could not be beaten by any other high card since the ace has the highest value.
2. One Pair - A card you have is the same as another card in your hand or a card on the board. For example, you have an king in your hand and there is an king on the board. This hand could be beaten by a higher pair, such as a pair of aces.
3. Two Pairs - One card in your hand matches a card on the board and the other card in your hand matches another card on the board. For example, you have a queen and a king in your hand and there is a queen and a king on the board. This hand could be beaten if someone had a pair of aces and a pair of 2s. The highest of the two pairs takes the pot.
4. Three of a kind - There is a combination of the cards in your hand and the cards on the board such that there are three of the same card. For example, you have a king in your hand and there are two kings on the board. This hand could be beaten if someone else had an ace in their hand and there were two aces on the board since the ace holds higher value than the king.
5. Straight - There is a combination of the cards in your hand and the cards on the board such that there are 5 cards in a row. For example, you have a 3 and a 4 and there is a 5, 6, and 7 on the board. This described hand would be beaten by a higher straight. Say we still have the 5, 6, and 7 on the board. The previously described hand would be beaten if someone had an 8 and 9, since it is a higher straight.
6. Flush - There is a combination of the cards in your hand and the cards on the board such that there are 5 cards of the same suit. For example, if there is a 5 of hearts, 10 of hearts, and jack of hearts on the board and you have a queen of hearts and king of hearts. However, again, the previously described hand would be beaten by someone who had a 2 of hearts and an ace of hearts, since they have the higher flush because the ace has a higher value than the king.
7. Full House - There is a combination of the cards in your hand and the cards on the board such that you have a pair and a three of a kind. For example, you have a 10 and jack in your hand. If there are two 10s on the board and a jack, then you would have a full house. This would be called jacks full of 10s. This hand could be beaten if someone had a pair of jacks in their hand. They would then have 10s full of jacks. This is the stronger hand since three of a kind jacks holds a higher value than three of a kind 10s.
8. Four of a kind - There is a combination of the cards in your hand and the cards on the board such that there are four of the same card. For example, you have two kings in your hand and there are two kings on the board. This hand could be beaten if someone had a pair of aces in their hand and there were two aces on the board, since aces have a higher value than kings.
9. Straight Flush - There is a combination of the cards in your hand and the cards on the board such that there are 5 cards in a row of the same suit. For example, you have a 3 of hearts and a 4 of hearts and there is a 5 of hearts, 6 of hearts, and 7 of hearts on the board. Again, this could be beaten if someone had an 8 of hearts and a 9 of hearts since it is the higher straight.


## End Game:

The players will continue to play hands until they are either out of money or are the last player standing. Once there is only one player remaining with money, the game ends.

This is an example of what the game ending looks like in the GUI:

![Alt text](/resources/endGameBoard.png)

# Open Design, Fail-Safe Defaults, and Economy of Mechanism Examples:

## Open Design:
The very nature of this software, the source code being available on GitHub, promotes there being an open design. Additionally, our implementations of clear/meaningful test cases, meaning names of variables, proper use of data structures, and the inclusion of a UML diagram aid in ensuring our code follows an Open Design.

1. Clear/meaningful test cases:
    - The following image illustrates how our test cases explain very clearly what they are testing for: ![Alt text](/resources/testCases.png). If these test cases were not clear, it would make it difficult to understand what the program was tested against. These tests were made with an adversarial mindset, and more have been added since the early drafts of this program.
2. Meaningful names of variables:
    - The following code is from the Player Class. This class contains variables that express their purpose in their name. The function names also imply their meaning just by their names. This helps to ensure our code remains clear:
    ```scala
    class Player(private val name: String) {
        private var hand: List[Card] = Nil
        private var money: Int = startingAmount
        private var fold: Boolean = false
        private var times: Int = 0
        private var strategy: Strategy = new FollowTheLeader()
        private var moneyBet: Int = 0

        /** Increments the times the player has played in one hand.
        */
        def addTimes: Unit = times += 1

        /** Decrements the times the player has played in one hand.
        */
        def subTimes: Unit = times -= 1

        /** Returns the amount of times the player has played in one hand.
        */
        def getTimes: Int = times

        /** Resets the number of times a player has played in one hand.
        */
        def resetTimes: Unit = times = 0

        /** Returns a player's current hand.
        */
        def getHand: List[Card] = hand
        /** Returns a player's current amount of money available.
        */
        def getMoney: Int = money

        /** Adds money to a player's account.
        * @param x money to add to a player's account.
        * @return Unit
        */
        def addMoney(x: Int): Unit = money += x

        /** Removes a player's money.
        * @param x money to remove from player's account.
        */
        def removeMoney(x: Int): Unit = money -= x

        /** Places a bet.
        * @param x money placed for the bet.
        * @return the amount of money bet.
        */
        def bet(x: Int): Int = {
            val moneyLeftAfterBet: Int = getMoney - x
            var output: Int = 0
            if (moneyLeftAfterBet > 0) {
            output = x
            } else {
            output = getMoney
            }
            removeMoney(output)
            Pot.addPot(output)
            Flags.setPreviousDecision("bet")
            Flags.setPreviousBet(true)
            moneyBet += output
            output
        }

        /** Shows the player's hand as a string.
        */
        def showHandString: String = {
            var output: String = name + " = "
            output += "(" + hand.mkString(", ") + ")"
            output
        }
        /** Resets a player's hand to be empty and resets their fold status.
        *
        */
        def resetHand(): Unit = {
            hand = Nil
            fold = false
        }
        /** Sets the player strategy.
         * @param strategy is the strategy to be used as a string
         */
        def setPlayerStrategy(strat: String): Unit = strat match {
            case "highCard" => strategy = new HighCard()
            case "aPair" => strategy = new APair()
            case "connectors" => strategy = new Connectors()
            case "followTheLeader" => strategy = new FollowTheLeader()
        }
    ```
3. Proper use of data structures:
    - While an array is usually capable of emulating most data structures, this project pairs the right data structure for each job based on the data structure's capability/purpose. For example, the `PlayerOrder` object extends Queues since a player order is simple a queue. Another example is that the `Deck` uses a Stack to hold the cards in a deck. Using a Stack allows the programmers to pop and add cards seamlessly. In the code below, using a stack allows the code to be more readable:
    ```scala
    /** Deals a card.
     * @return A card.
     */
    def deal(): Card = stack.pop()
    ```
    Since dealing is the same as just popping off a stack, this code is exceptionally readable compared to if another data structure was used.


## Fail-Safe Defaults:
In order to reduce access to only necessary parts of the code, careful use of encapsulation ensured to reduce parts of the code's exposure. In the example below, the `evalEngine`'s use of private methods ensure that only certain functions are available publicly to the codebase:
```scala
/** Computes the winner of a given hand.
 * @return the Long value of a hand's strength.
 */
def valueHand: Long = {
if ( isFlush && isStraight) STRAIGHTFLUSH + valueHighCard
else if (is4s) FOUROFAKIND + valueHighCard
else if (isFullHouse) FULLHOUSE + valueHighCard
else if (isFlush) FLUSH + valueHighCard
else if (isStraight) STRAIGHT + valueHighCard
else if (is3s) SET + valueHighCard
else if (is22s) TWOPAIRS + valueHighCard
else if (is2s) ONEPAR + valueHighCard
else valueHighCard
}
/** Sorts a hand of Cards from low to high by rank.
 * @param h A hand of cards.
 * @return A sorted hand.
 */
private def sortByRank(h: Array[Card]): Array[Card] = h.sortWith(sortRank(_, _))

/** A helper to sort a hand of Cards from low to high by Rank.
 * @param card1 is the first card.
 * @param card2 is the next card to be compared.
 * @return Which suit is bigger as a bool.
 */
private def sortRank(card1: Card, card2: Card): Boolean = {
card1.toInt() < card2.toInt()
}

/** A helper to sort a hand of Cards from low to high by Suit.
 * @param card1 is the first card.
 * @param card2 is the next card to be compared.
 * @return Which suit is bigger as a bool.
 */
private def sortSuit(card1: Card, card2: Card): Boolean = {
card1.getSuit < card2.getSuit
}

/** Sorts a hand of Cards from low to high by suit.
 * @param h A hand of cards.
 * @return A sorted hand.
 */
private def sortBySuit(h: Array[Card]): Array[Card] = h.sortWith(sortSuit(_, _))

/** Returns the score value of a high card as an integer.
 * @param h The hand of cards of type array
 */
private def valueHighCard: Long = {
this.playersHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
}
```
Notice that the only publicly available method is the `valueHand` method. Since the other methods solely contribute to `valueHand`, there is no reason that these methods should be accessed by anything outside of the class. Also for the class card, the variables are by default private. In order to access them, one must call a helper function:
```scala
class Card(
    private val rank: String,
    private val suit: Char,
    private var flipped: Boolean = false
) {

  /** Return the card's String representation.
   */
  def getCard: String = {
    var result: String = ""
    if (!flipped) result = rank.toString + suit.toString
    else result = "HIDDEN"
    result
  }

  /** Flips a card.
   * @return Unit.
   */
  def flip(): Unit = {
    flipped = !flipped
  }

  /** Resets a card's flip status to false
   * @return Unit.
   */
  def reset(): Unit = flipped = false

  // These methods only exist since parameters are private. Check later.
  /** Returns a card's rank.
   * @return The card's ranks as a char.
   */
  def getRank: String = rank

  /** Returns a card's suit.
   * @return the card's suit as a char.
   */
  def getSuit: Char = suit
}
```

## Economy of Mechanism
Finally, the strategies were created/structured in such a way that it ensures each strategy will have the same properties/structure. While each strategy is doing something different, their class structure is the same.

Additionally, building this program with object oriented programming in mind ensures that minimal code is needed. For example, a `Card` is a class that contains certain properties. By making it a class, we can make many instances of the class and reuse the class's properties rather than needing to rewrite code.

Finally, if one looks through the code, there are plenty of instances where code is composed into a function for reusability. By reducing the "copy and pasting" of code, there are less chances of errors, vulnerabilities, and bugs to nest inside of the code.

## Works Cited:

1. Nicholas Liebers. 18 January 2022. Assistance given to author via teams call. CDT Liebers assisted me by cross checking my product against the rubric. He suggested that I break up my game flow section from my previous commit to make it less blocky and more readable. He also suggested that I make my player hands in my test code tuples to increase readability. Finally, he suggested that I make the initial state to when the cards have been dealt and the initial antes have been put in the pot. West Point, NY.

2. https://www.mathcs.emory.edu/~cheung/Courses/170/Syllabus/10/pokerCheck.html. 05 APR 2022. Assistance give to the author via website. This source played an integral part in our project. In order to calculate the strength of a had to determine a winner, we used this source's algorithm. We essentially copied the code from this website. However, this source provides code that was written in java and for only 5 cards. Therefore, we were required to not only translate it to scala, but we were required to also adjust so that it worked with 7 cards. While this task might appear trivial, it was not, and it required a large amount testing/workshopping to get the required result. We deemed it appropriate to use this source since this class is not focused on algorithms. West Point, NY. 12 April 2022.