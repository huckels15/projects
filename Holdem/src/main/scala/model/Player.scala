package model

/** A player in the poker game.
  *
  * @constructor
  *   create a new player with a hand, money, and ability to fold.
  * @param name
  *   the player's name.
  */
class Player(private val name: String) {
  private var hand: List[Card] = Nil
  private var money: Int = startingAmount
  private var fold: Boolean = false
  private var times: Int = 0
  private var strategy: Strategy = new FollowTheLeader()
  private var moneyBet: Int = 0

  /** Increments the times the player has played in one hand.
    */
  def addTimes: Unit = times += 1

  /** Decrements the times the player has played in one hand.
    */
  def subTimes: Unit = times -= 1

  /** Returns the amount of times the player has played in one hand.
    */
  def getTimes: Int = times

  /** Resets the number of times a player has played in one hand.
    */
  def resetTimes: Unit = times = 0

  /** Returns a player's current hand.
    */
  def getHand: List[Card] = hand

  /** Returns a player's current amount of money available.
    */
  def getMoney: Int = money

  /** Adds money to a player's account.
    * @param x
    *   money to add to a player's account.
    * @return
    *   Unit
    */
  def addMoney(x: Int): Unit = money += x

  /** Removes a player's money.
    * @param x
    *   money to remove from player's account.
    */
  def removeMoney(x: Int): Unit = money -= x

  /** Places a bet.
    * @param x
    *   money placed for the bet.
    * @return
    *   the amount of money bet.
    */
  def bet(x: Int): Int = {
    val moneyLeftAfterBet: Int = getMoney - x
    var output: Int = 0
    if (moneyLeftAfterBet > 0) {
      output = x
    } else {
      output = getMoney
    }
    removeMoney(output)
    Pot.addPot(output)
    Flags.setPreviousDecision("bet")
    Flags.setPreviousBet(true)
    moneyBet += output
    output
  }

  /** Shows the player's hand as a string.
    */
  def showHandString: String = {
    var output: String = name + " = "
    output += "(" + hand.mkString(", ") + ")"
    output
  }

  /** Adds a card to a player's hand.
    * @param card
    *   the card added to the player's hand.
    */
  def addHand(card: Card): Unit = {
    hand = card :: hand
  }

  /** Resets a player's hand to be empty and resets their fold status.
    */
  def resetHand(): Unit = {
    hand = Nil
    fold = false
  }

  /** Adds a player's ante to the pot.
    */
  def anteUp: Unit = {
    Pot.addPot(ante) // Remove magic number.
  }

  /** Evaluates a player's hand strength.
    * @return
    *   integer value for a player's hand strength.
    */
  def evalHand: Long = {
    val engine: evalEngine = new evalEngine(hand, Board.getBoard)
    // System.out.println(this.getName)
    // System.out.println(engine.valueHand.toString())
    engine.valueHand
  }

  /** Returns player's name.
    */
  def getName: String = name

  /** Changes a player's fold status to true.
    */
  def doFold(): Unit = {
    fold = true
    hand = Nil
    PlayerOrder.removePlayer()
    Flags.setPreviousDecision("fold")
    Flags.setPreviousFold(true)
  }

  /** Sets player's money to some integer value.
    * @param amount
    *   is the amount of money to set a player to
    */
  def setMoney(amount: Int): Unit = {
    money = amount
  }

  /** Resets player's money to 1000.
    */
  def resetMoney(): Unit = {
    money = startingAmount
  }

  /** Sets the fold status boolean to true of false
    * @param bool
    *   is the input fold status to change to
    * @return
    *   boolean of current fold status
    */
  def setFoldStatus(bool: Boolean): Boolean = {
    fold = bool
    fold
  }

  /** Sets the player strategy.
    * @param strategy
    *   is the strategy to be used as a string
    */
  def setPlayerStrategy(strat: String): Unit = strat match {
    case "highCard"        => strategy = new HighCard()
    case "aPair"           => strategy = new APair()
    case "connectors"      => strategy = new Connectors()
    case "followTheLeader" => strategy = new FollowTheLeader()
  }

  /** Returns the player strategy as a strategy object
    */
  def getPlayerStrategy: Strategy = {
    strategy
  }

  /** Overrides the current hand and changes hand to new inputted hand
    * @param input
    *   is a new hand that is a list
    */
  def changeCurrentHand(input: List[Card]): Unit = {
    hand = input
  }

  /** Sets the previousMove of the hand to check.
    */
  def check: Unit = {
    Flags.setPreviousDecision("check")
  }

  /** Converts player to string.
    * @return
    *   the player's name.
    */
  override def toString(): String = getName

}
