package model

/** An abstract class for our strategies.
  * @constructor
  *   creates a name val that is the name of the strategy.
  */
abstract class Strategy {
  private var name = ""
  private var hasBet = false

  /** Sets the hasBet variable to an input.
    * @param input
    *   is the input that hasBet will be set to.
    */
  def setHasBet(input: Boolean): Unit

  /** Returns a String of the previousDecision in the hand.
    */
  def move: String = Flags.getPreviousDecision

  /** Provides logic for how the player does moves according to this strategy.
    */
  def doStrategy(playerOrderLength: Int): Unit

  /** Returns the move type as a string.
    */
  def getMoveType: String

  /** Defines how to turn the object into a String.
    * @return
    *   the object as a String.
    */
  override def toString(): String
}

/** A follow the leader strategy
  * @constructor
  *   creates a name variable that defaults to "default."
  */
class FollowTheLeader extends Strategy {

  /** Returns a String of the previousDecision in the hand.
    */
  override def move: String = Flags.getPreviousDecision
  private var name = "default"
  private var hasBet = false

  /** Sets the hasBet variable to an input.
    * @param input
    *   is the input that hasBet will be set to.
    */
  override def setHasBet(input: Boolean): Unit = hasBet = input

  /** Returns the move type as a string.
    */
  override def getMoveType: String = move

  /** Provides logic for how the player does moves according to this strategy.
    */
  override def doStrategy(playerOrderLength: Int): Unit = move match {
    case "bet" => {
      PlayerOrder.current.bet(defaultBet)
    }
    case "fold" => {
      if (playerOrderLength > 1) PlayerOrder.current.doFold()
    }
    case "check" => PlayerOrder.current.check
  }

  /** Defines how to turn the object into a String.def
    * @return
    *   the object as a String.
    */
  override def toString(): String = {
    name
  }
}

/** A strategy if a player has a high card
  * @constructor
  *   creates a variable that indicates if the player has bet during a hand and
  *   the name that defaults to "highCard".
  */
class HighCard extends Strategy {
  private var hasBet = false
  private var name = "highCard"

  /** Sets the hasBet variable to an input.
    * @param input
    *   is the input that hasBet will be set to.
    */
  override def setHasBet(input: Boolean): Unit = hasBet = input

  /** Returns the move type as a string.
    */
  override def getMoveType: String = move

  /** Provides logic for how the player does moves according to this strategy.
    */
  override def doStrategy(playerOrderLength: Int): Unit = {
    var break = false
    for { card <- PlayerOrder.current.getHand if !break } {
      if (card.toInt() >= 10 && !hasBet) {
        PlayerOrder.current.bet(defaultBet)
        break = true
        hasBet = true
      } else if (Flags.getPreviousBet) PlayerOrder.current.doFold()
      else PlayerOrder.current.check
    }
  }

  /** Defines how to turn the object into a String.def
    * @return
    *   the object as a String.
    */
  override def toString(): String = {
    name
  }
}

/** A strategy when a player has two pairs
  * @constructor
  *   creates a variable that sets the name that defaults to "aPair".
  */
class APair extends Strategy {
  private var name = "aPair"
  private var hasBet = false

  /** Sets the hasBet variable to an input.
    * @param input
    *   is the input that hasBet will be set to.
    */
  override def setHasBet(input: Boolean): Unit = hasBet = input

  /** Returns the move type as a string.
    */
  override def getMoveType: String = move

  /** Provides logic for how the player does moves according to this strategy.
    */
  override def doStrategy(playerOrderLength: Int): Unit = {
    var hasPair = false
    for (card <- PlayerOrder.current.getHand) {
      for (card1 <- Board.getBoard) {
        if (card.getRank == card1.getRank) hasPair = true
      }
    }
    if (
      PlayerOrder.current.getHand.head.getRank == PlayerOrder.current.getHand.tail.head.getRank
    ) hasPair = true
    if (hasPair) {
      PlayerOrder.current.bet(defaultBet)
    } else if (Flags.getPreviousBet) PlayerOrder.current.doFold()
    else PlayerOrder.current.check
  }

  /** Defines how to turn the object into a String.def
    * @return
    *   the object as a String.
    */
  override def toString(): String = {
    name
  }
}

/** A strategy when a player has two cards in sequential order
  * @constructor
  *   creates a variable that indicates if the player has bet during a hand and
  *   the name that defaults to "connectors".
  */
class Connectors extends Strategy {

  private var name = "connectors"
  private var hasBet = false

  /** Sets the hasBet variable to an input.
    * @param input
    *   is the input that hasBet will be set to.
    */
  override def setHasBet(input: Boolean): Unit = hasBet = input

  /** Returns the move type as a string.
    */
  override def getMoveType: String = move

  /** Provides logic for how the player does moves according to this strategy.
    */
  override def doStrategy(playerOrderLength: Int): Unit = {
    var hasConnection = false
    if (
      PlayerOrder.current.getHand.head
        .toInt() == PlayerOrder.current.getHand.tail.head
        .toInt() + 1 || PlayerOrder.current.getHand.head
        .toInt() == PlayerOrder.current.getHand.tail.head.toInt() - 1
    ) hasConnection = true
    if (!hasBet && !Flags.getPreviousBet) {
      PlayerOrder.current.bet(defaultBet)
      hasBet = true
    } else if (Flags.getPreviousBet) PlayerOrder.current.doFold()
    else PlayerOrder.current.check
  }

  /** Defines how to turn the object into a String.def
    * @return
    *   the object as a String.
    */
  override def toString(): String = {
    name
  }
}
