package model

//*****************************************************************************
// SEE README FOR WORKS CITED!!!
//*****************************************************************************
/** Evaluates the Strength of a Poker Hand.
 * @param playersHand The Cards a player has.
 * @param hand The current hand in a game.
 * @constructor Creates an array that holds 7 cards.
 */
class evalEngine(playersHand: List[Card], hand: Array[Card]) {

  private val h: Array[Card] = new Array[Card](7)
  initH()

  /** Combines the board hand and playerHand into one array.def
   *
   */
  private def initH(): Unit = {
    var i = 0
    for (player <- this.playersHand) {
      h(i) = player
      i += 1
    }
    for (player <- this.hand) {
      h(i) = player
      i += 1
    }
  }

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

  /** Returns True if hand is 4 of a kind
   * @param h The hand of cards of type array.
   */
  private def is4s: Boolean = {
    if (this.h.length != 7) false
    else {
      val h = sortByRank(this.h)
      var output = false
      for (i <- 0 until h.length - 3) output = output || h(i).getRank == h(i+1).getRank && h(i+1).getRank == h(i+2).getRank && h(i+2).getRank == h(i+3).getRank
      output
      }
  }

  /** Returns True if hand is Full House.
   * @param h The hand of cards of type array.
   */
  private def isFullHouse: Boolean = {
    if (this.h.length != 7) false
    else {
      val h = sortByRank(this.h)
      val a1: Boolean = h(0).getRank == h(1).getRank && h(1).getRank == h(2).getRank && h(3).getRank == h(4).getRank
      val a2: Boolean = h(0).getRank == h(1).getRank && h(1).getRank == h(2).getRank && h(4).getRank == h(5).getRank
      val a3: Boolean = h(0).getRank == h(1).getRank && h(1).getRank == h(2).getRank && h(5).getRank == h(6).getRank
      val a4: Boolean = h(2).getRank == h(3).getRank && h(3).getRank == h(4).getRank && h(5).getRank == h(6).getRank
      val a5: Boolean = h(0).getRank == h(1).getRank && h(2).getRank == h(3).getRank && h(3).getRank == h(4).getRank
      val a6: Boolean = h(0).getRank == h(1).getRank && h(3).getRank == h(4).getRank && h(4).getRank == h(5).getRank
      val a7: Boolean = h(0).getRank == h(1).getRank && h(4).getRank == h(5).getRank && h(5).getRank == h(6).getRank
      val a8: Boolean = h(2).getRank == h(3).getRank && h(4).getRank == h(5).getRank && h(5).getRank == h(6).getRank
      val a9: Boolean = h(1).getRank == h(2).getRank && h(4).getRank == h(5).getRank && h(5).getRank == h(6).getRank
      val a10: Boolean = h(1).getRank == h(2).getRank && h(2).getRank == h(3).getRank && h(5).getRank == h(6).getRank
      a1 || a2 || a3 || a4 || a5 || a6 || a7 || a8 || a9 || a10
    }
  }

  /** Returns True if hand is 3 of a kind
   * @param h The hand of cards of type array.
   */
  private def is3s: Boolean = {
    if (this.h.length != 7) false
    else if (is4s || isFullHouse) false
    else {
      var output = false
      val h = sortByRank(this.h)
      for (i <- 0 until h.length - 2) output = output || h(i).getRank == h(i+1).getRank && h(i+1).getRank == h(i+2).getRank
      output
    }
  }

  /** Returns True if hand is 2 pairs
   * @param h The hand of cards of type array.
   */
  private def is22s: Boolean = {
    if (this.h.length != 7) false
    else if (is4s|| isFullHouse || is3s) false
    else {
      val h = sortByRank(this.h)
      val a1: Boolean = h(0).getRank == h(1).getRank && h(2).getRank == h(3).getRank
      val a2: Boolean = h(0).getRank == h(1).getRank && h(3).getRank == h(4).getRank
      val a3: Boolean = h(0).getRank == h(1).getRank && h(4).getRank == h(5).getRank
      val a4: Boolean = h(0).getRank == h(1).getRank && h(5).getRank == h(5).getRank
      val a5: Boolean = h(1).getRank == h(2).getRank && h(5).getRank == h(6).getRank
      val a6: Boolean = h(2).getRank == h(3).getRank && h(5).getRank == h(6).getRank
      val a7: Boolean = h(3).getRank == h(4).getRank && h(5).getRank == h(6).getRank
      val a8: Boolean = h(2).getRank == h(3).getRank && h(4).getRank == h(5).getRank
      val a9: Boolean = h(1).getRank == h(2).getRank && h(3).getRank == h(4).getRank
      a1 || a2 || a3 || a4 || a5 || a6 || a7 || a8 || a9
    }
  }

  /** Returns True if hand has 1 pair.
   * @param h The hand of cards of type array.
   */
  private def is2s: Boolean = {
    if (this.h.length != 7) false
    else if (is4s || isFullHouse || is3s || is22s) false
    else {
      val h = sortByRank(this.h)
      var output = false
      for (i <- 0 until h.length - 1) output = output || h(i).getRank == h(i+1).getRank
      output
    }
  }

  /** Returns True if hand is a flush.
   * @param h The hand of cards of type array.
   */
  private def isFlush: Boolean = {
    if (this.h.length != 7) false
    else {
      val h = sortBySuit(this.h)
      h(0).getSuit == h(4).getSuit || h(1).getSuit == h(5).getSuit || h(2).getSuit == h(6).getSuit
    }
  }

  /** Returns True if hand is a straight
   * @param h The hand of cards of type array.
   */
  private def isStraight: Boolean = {
    val h = sortByRank(this.h)
    var a = false
    var b = false
    var output = false
    if (this.h.length != 7) false
    else {
      if (h(6).getRank == "A") {
          a = h(0).getRank == "2" && h(1).getRank == "3" && h(2).getRank == "4" && h(3).getRank == "5"
          b = h(2).getRank == "10" && h(3).getRank == "J" && h(4).getRank == "Q" && h(5).getRank == "K"
        }
      var j = 0
      while (j < 3) {
        var inOut = true
        var testRank = h(j).toInt() + 1
        for (i <- 1 until 5) {
          if (h(i + j).toInt() != testRank) inOut = false
          testRank += 1
        }
        j += 1
        output = output || inOut
      }
        output || a || b
    }
  }
}
