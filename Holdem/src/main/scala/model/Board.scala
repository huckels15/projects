package model

/** The game board in the poker game.
  *
  * @constructor
  *   Creates a board size, and an array of Cards with the board size.
  */
object Board {

  private var boardCard = 3
  // Build Board
  private val size: Int = 5
  // May make this private again and use function to help in implementation
  private val board: Array[Card] = new Array[Card](size)

  /** Returns the board in string form.
    */
  def showBoardString: String = {
    var output: String = "Board:\n"
    output += board.mkString(", ") + "\n"
    output
  }

  /** Fills the game board with cards.
    * @return
    *   Unit.
    */
  def fillGameBoard(): Unit = {
    for (i <- 0 until size) board(i) = Deck.deal()
    for (i <- 3 until size) board(i).flip()
  }

  /** Resets the game board to all nulls
    * @return
    *   Unit.
    */
  def resetGameBoard(): Unit = {
    for (i <- 0 until board.length) {
      board(i) = null
      setBoardCard(3)
    }
    setBoardCard(3)
    PlayerOrder.setPlayerCount(0)
  }

  /** Returns the boardCard index as an integer.
    */
  def getBoardCard: Int = boardCard

  /** Sets the boardCard index to an integer.
    * @param x
    *   is the integer to set boardCard to.
    */
  def setBoardCard(x: Int): Unit = boardCard = x

  /** Returns the board as an array of cards.
    */
  def getBoard: Array[Card] = board
}
