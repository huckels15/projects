package model

/** A trait that has the lengthOfPlayerOrder.
  * @constructor
  *   Sets the lengthOfPlayerOrder to 0
  */
trait Length {
  protected var lengthOfPlayer: Int = 0
}

/** A trait that controls the amount of moves performed at any time.
  * @constructor
  *   Sets the playerCount to 0.
  */
trait PlayerCount {
  protected var playerCount: Int = 0

  /** Sets the playerCount to a certain integer
    * @param x
    *   is the value playerCount is set to
    */
  def setPlayerCount(x: Integer): Unit = playerCount = x

  /** Returns the playerCount as an integer
    */
  def getPlayerCount: Integer = playerCount
}

/** An object that contains and controls the player order as a Queue.
  * @constructor
  *   Enqueue the following players: Jacob, John, Bob, and Tom and set
  *   playerCount to 0.
  */
object PlayerOrder
    extends scala.collection.mutable.Queue[Player]
    with Length
    with PlayerCount {
  resetPlayerOrder()
  var lastMan: Player = this.last

  /** Advances the player order by 1.
    * @return
    *   Unit.
    */
  def advancePlayerOrder(): Unit = this.enqueue(this.dequeue())

  /** Returns a string of the player order.
    */
  def showPlayerOrderString: String = this.mkString(", ")

  /** Returns a player who is currently 1st in the player order.
    */
  def current: Player = this.head

  /** Removes a player from the order.
    * @return
    *   The player who was removed.
    */
  def removePlayer(): Player = {
    lengthOfPlayer -= 1
    if (this.current == this.lastMan) {
      this.lastMan = this.last
      this.dequeue()
    } else this.dequeue
  }

  /** Resets the player order to default with new player objects.
    */
  def resetPlayerOrder(): Unit = {
    if (this.nonEmpty) {
      this.removeAll()
      lengthOfPlayer = 0
    }
    Players.createPlayers()
    for (player <- Players.getGamePlayers) {
      this.enqueue(player)
      lengthOfPlayer += 1
    }
    setPlayerCount(0)
    lastMan = this.last
  }

  /** Resets the player order to the default, but does not create new player
    * objects.
    */
  def resetForHand(): Unit = {
    if (this.nonEmpty) {
      this.removeAll()
      lengthOfPlayer = 0
    }
    for (player <- Players.getGamePlayers) {
      if (player.getMoney > 0) {
        this.enqueue(player)
        lengthOfPlayer += 1
      }
    }
    lastMan = this.last
  }

  /** Returns the length of the PlayerOrder
    * @return
    *   int
    */
  override def length: Int = lengthOfPlayer
}
