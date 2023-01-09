package model

/** An object that shows how much money each player has.
  */
object Scoreboard {

  /** Returns a String that contains the amount of money each player has.
    * @return
    *   A String of the form "Player's Money:\n Jacob = {amount of money}, ..."
    */
  def showString: String = {
    var output: String = "Player's Money:\n"
    for (player <- Players.getGamePlayers)
      output += player.getName + " = " + player.getMoney.toString() + ", "
    output = output.slice(0, output.length - 2) + "\n"
    output
  }

  def showString_arr: scala.collection.mutable.ArrayBuffer[String] = {
    var output = scala.collection.mutable.ArrayBuffer.empty[String]
    for (player <- Players.getGamePlayers)
      output += player.getName + " : " + player.getMoney.toString()
    output
  }
}
