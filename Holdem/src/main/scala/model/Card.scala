package model

/** A card in the game of poker.
  * @param rank
  *   The rank of the card ('A', '1', '2', '3', '4', '5', '6', '7', '8', '9',
  *   'J', 'Q', 'K').
  * @param suit
  *   The suit of the card ('S', 'H', 'D', 'C').
  * @param flipped
  *   If the back of the card is showing.
  */
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
    * @return
    *   Unit.
    */
  def flip(): Unit = {
    flipped = !flipped
  }

  /** Resets a card's flip status to false
    * @return
    *   Unit.
    */
  def reset(): Unit = flipped = false

  // These methods only exist since parameters are private. Check later.
  /** Returns a card's rank.
    * @return
    *   The card's ranks as a char.
    */
  def getRank: String = rank

  /** Returns a card's suit.
    * @return
    *   the card's suit as a char.
    */
  def getSuit: Char = suit

  /** Controls how a Card is converted to an integer.
    * @return
    *   Returns the Card Rank as an int.
    */
  def toInt(): Int = this.getRank match {
    case "2"  => 2
    case "3"  => 3
    case "4"  => 4
    case "5"  => 5
    case "6"  => 6
    case "7"  => 7
    case "8"  => 8
    case "9"  => 9
    case "10" => 10
    case "J"  => 11
    case "Q"  => 12
    case "K"  => 13
    case "A"  => 14
  }

  /** Returns a string representation of this object.
    */
  override def toString(): String = getCard

  /** Returns a true if the card is flipped and false if not.
    */
  def getFlipped: Boolean = flipped

}
