package model

/** A pot of money in poker.
  * @constructor
  *   Initializes the intial money in the pot.
  */
object Pot {
  private var amount: Int = 0

  /** Return amount of money in the pot.
    * @return
    *   Money as an Int.
    */
  def getPot: Int = amount

  /** Prints the amount of money in the pot.
    * @return
    *   Unit.
    */
  def showPot: Unit = print(amount.toString())

  /** Adds money to the pot.
    * @return
    *   Unit.
    */
  def addPot(x: Int): Unit = amount += x

  /** Subtracts money to the pot.
    * @return
    *   Unit.
    */
  def subtractPot(x: Int): Unit = amount -= x

  /** Resets pot size to 0
    * @return
    *   Unit.
    */
  def resetPot(): Unit = amount = 0

  /** Returns a string representation of this object.
    */
  override def toString(): String = getPot.toString()
}
