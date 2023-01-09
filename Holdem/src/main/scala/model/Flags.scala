package model

/** An object that contains various global flags that must be accounted for
  * throughout a game.
  * @constructor
  *   creates a var that contains the previous move outcome, a var that is true
  *   if a bet occurred during this hand, and a var that is true if a fold has
  *   occurred during this hand.
  */
object Flags {
  private var previousDecision: String = "bet"
  private var previousBet: Boolean = false
  private var previousFold: Boolean = false
  private var handWinner: String = ""

  /** Sets the handWinner to a string.
    * @param player
    *   is the player to change the hand winner to
    */
  def setHandWinner(player: String): Unit =
    handWinner = player

  /** Returns the hand winner as a string.
    */
  def getHandWinner: String = handWinner

  /** Returns a string of what the previous move was on the board (bet, check,
    * or fold).
    */
  def getPreviousDecision: String = previousDecision

  /** Manually sets the previousDecision to an input (bet, check, or fold).
    * @param input
    *   is the bet, check, or fold that is the flag previousBet will be set to.
    */
  def setPreviousDecision(input: String): Unit = previousDecision = input

  /** Resets the previousDecision variable back to "bet".
    */
  def reset(): Unit = setPreviousDecision("bet")

  /** Returns a boolean that is true if a player has.
    */
  def getPreviousBet: Boolean = previousBet

  /** Sets the previousBet flag.
    * @param input
    *   is the value to change previousBet to (true or false).
    */
  def setPreviousBet(input: Boolean): Unit = {
    previousBet = input
  }

  /** Resets previousBet to false.
    */
  def resetPreviousBet: Unit = setPreviousBet(false)

  /** Returns the previousFold flag as a boolean.
    */
  def getPreviousFold: Boolean = previousFold

  /** Sets the previousFold flag to an input.
    * @param input
    *   is the desired value to set previousFold to (true or false).
    */
  def setPreviousFold(input: Boolean) = {
    previousFold = input
  }

  /** Resets the previousFold flag to false.
    */
  def resetPreviousFold: Unit = setPreviousFold(false)
}
