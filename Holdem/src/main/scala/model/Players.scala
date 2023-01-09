package model

/** An object that contains the player objects in a game.
  * @constructor
  *   creates an array that contains the players in the game.
  */
object Players {

  private val gamePlayers: Array[Player] = new Array[Player](numPlayers)

  /** Creates players and stores them in an array.
    */
  def createPlayers(): Unit = {
    for (i <- 0 until numPlayers) gamePlayers(i) = new Player(playerNames(i))
  }

  /** Returns an array of the current players.
    */
  def getGamePlayers: Array[Player] = gamePlayers
}
