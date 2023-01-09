package model

/** A dealer in a poker game. A dealer deals cards in poker.
  * @constructor
  *   create a default amount for ante.
  */
object Dealer {

  /** Deals cards to each player in the Player Order.
    * @return
    *   Unit.
    */
  def deal: Unit = {
    for (_ <- 0 until 2) {
      PlayerOrder.foreach(player => player.addHand(Deck.deal()))
    }
  }

  /** Collects an ante from each player in the Player Order.
    * @return
    *   Unit.
    */
  def collectAnte: Unit = {
    for (player <- PlayerOrder) {
      val extraMoney: Int = player.getMoney - ante
      if (extraMoney >= 0)
        Pot.addPot(ante)
        player.removeMoney(ante)
    }
  }

  /** Resets all of the player's hands to nothing.
    * @return
    *   Unit.
    */
  def reset: Unit = {
    Players.getGamePlayers.foreach(player => {
      player.resetHand()
      player.resetMoney()
    })
    Pot.resetPot()
  }

  /** Resets Dealer for a new hand
    * @return
    *   Unit.
    */
  def resetHand(): Unit = {
    for (player <- Players.getGamePlayers) {
      player.resetHand()
    }
    Pot.resetPot()
  }

  /** Determines the winner of a hand.
    * @return
    *   Name of the player who won the hand.
    */
  def handWinner: String = {
    // Default/poor implementation
    var winner: String = ""
    var max: Long = 0L
    // Implement Ties later
    // val ties: List
    for (player <- PlayerOrder) {
      val value: Long = player.evalHand
      if (value >= max) {
        winner = player.toString()
        max = value
      }
    }
    winner
  }
}
