package model

/** An object that shows the size of the pot in poker.
  */
object PotBoard {

  /** Returns a String that contains the current size of the pot.
    * @return
    *   A String of the form "Current Pot Size: {the pot size}"
    */
  def showString: String = {
    val output: String = "Current Pot Size: " + Pot.toString() + "\n"
    output
  }
}
