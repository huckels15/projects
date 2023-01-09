package model

/** An object that prints the player's hands.
  */
object PlayerHands {

  /** Returns a String representation of the player's hands.
    * @return
    *   A String of the form "Player's Hands:\n Jacob = {hand}, ..."
    */
  def showString: String = {
    var output: String = "Player's Hands:\n"
    for (player <- Players.getGamePlayers)
      output += player.showHandString + ", "
    output = output.slice(0, output.length - 2) + "\n"
    output
  }

  /** Returns an array of each player's hands as a String.
    */
  def showString_arr: scala.collection.mutable.ArrayBuffer[List[Card]] = {
    var output = scala.collection.mutable.ArrayBuffer.empty[List[Card]]
    for (player <- Players.getGamePlayers) output += player.getHand
    output
  }
}
