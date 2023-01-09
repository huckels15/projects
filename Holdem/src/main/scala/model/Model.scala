package model

import controller._

/** The menu in the poker game.
  * @constructor
  *   creates a var times to count how many times the model has iterated through
  *   the deck and to set stop to false.
  */
class Model {
  private var times: Int = 0
  private var stop: Boolean = false

  /** Returns a String of the player order.
    * @return
    *   A string of the form "Jacob, John, Bob, Tom".
    */
  def showPlayerOrder: String = {
    PlayerOrder.showPlayerOrderString
  }

  /** Advances the player order by 1.
    * @return
    *   Unit.
    */
  def advancePlayerOrder: Unit = {
    PlayerOrder.advancePlayerOrder()
  }

  /** Returns a String of each player's strategies.
    */
  def showStrategies: String = {
    var output = ""
    for (player <- PlayerOrder) {
      output += player.getName + ": " + player.getPlayerStrategy
        .toString() + "\n"
    }
    output
  }

  /** Returns a String of the game area.
    * @return
    *   A string of the board, the scoreboard, the player hands, and the amount
    *   of money in the pot.
    */
  def showGameArea: String = {
    var gameArea = ""
    gameArea += Board.showBoardString
    gameArea += "\n"
    gameArea += Scoreboard.showString
    gameArea += "\n"
    gameArea += PlayerHands.showString
    gameArea += "\n"
    gameArea += PotBoard.showString
    gameArea
  }

  /** Initializes the Menu.
    * @return
    *   Unit.
    */
  def init: Unit = {
    PlayerOrder.resetPlayerOrder()
    Dealer.reset
    Board.resetGameBoard()
    Deck.buildDeck()
    Dealer.deal
    Board.fillGameBoard()
    Dealer.collectAnte
    Flags.reset()
    Flags.resetPreviousBet
    Flags.resetPreviousFold
  }

  /** Initializes the menu for a new round
    * @return
    *   Unit.
    */
  def initRound: Unit = {
    PlayerOrder.resetForHand()
    Dealer.resetHand()
    Board.resetGameBoard()
    Deck.buildDeck()
    if (PlayerOrder.length > 1) {
      Dealer.deal
      Board.fillGameBoard()
      Dealer.collectAnte
    }
    for (player <- PlayerOrder) {
      player.resetTimes
      if (
        player.getPlayerStrategy
          .toString() == "highCard" || player.getPlayerStrategy
          .toString() == "connectors"
      ) player.getPlayerStrategy.setHasBet(false)
    }
    times = 0
    stop = true
    Flags.resetPreviousFold
    Flags.resetPreviousBet
  }

  /** Checks who is winning (who has the most money).
    * @return
    *   A string of the player who has the most money.
    */
  def checkForWinner: String = {
    var output: String = "none"
    for (player <- PlayerOrder) {
      if (player.getMoney == winMoneyAmount) output = player.toString()
    }
    output
  }

  /** Performs a player move.
    * @return
    *   Unit.
    */
  def doMove: Unit = {
    val boardCard: Int = Board.getBoardCard
    val playerOrderLength: Int = PlayerOrder.length
    PlayerOrder.current.addTimes
    if (PlayerOrder.current.getTimes > 2 || playerOrderLength == 1) {
      Flags.setHandWinner(
        if (playerOrderLength != 1) Dealer.handWinner
        else PlayerOrder.current.getName
      )
      for (player <- PlayerOrder) {
        if (Flags.getHandWinner == player.toString())
          player.addMoney(Pot.getPot)
      }
      initRound
    } else {
      if (PlayerOrder.current == PlayerOrder.lastMan) {
        Board.getBoard(boardCard).flip()
        Board.setBoardCard(boardCard + 1)
      }
      PlayerOrder.current.getPlayerStrategy.doStrategy(playerOrderLength)
      if (PlayerOrder.current == PlayerOrder.lastMan) {
        Flags.resetPreviousBet
        Flags.resetPreviousFold
      }
      if (Flags.getPreviousDecision != "fold") PlayerOrder.advancePlayerOrder()
    }
  }

  /** Performs a turn where 4 moves are done.
    * @return
    *   Unit.
    */
  def doTurn: Unit = {
    // If there is a winner, must break
    val length = PlayerOrder.length
    var first = PlayerOrder.current.getName
    var last = PlayerOrder.lastMan.getName
    if first == last then doMove
    while (first != last) {
      first = PlayerOrder.current.getName
      last = PlayerOrder.lastMan.getName
      doMove
    }
  }

  /** Performs 1 round where each player has the option to go twice.
    * @return
    *   Unit
    */
  def doRound: Unit = {
    doTurn
    doTurn
  }

  /** Performs a whole game until there is a winner.
    * @return
    *   Unit.
    */
  def doGame: Unit = {
    init
    while (checkForWinner == "none") {
      doRound
    }
  }

  /** Returns an ArrayBuffer that contains the names of each player in the game.
    * Used for the GUI.
    */
  def ind_players: scala.collection.mutable.ArrayBuffer[String] = {
    // May be able to remove since this has already been created
    Scoreboard.showString_arr
  }

  /** Returns the strategy of a player at any given time in an ArrayBuffer. Used
    * for the GUI.
    */
  def strats: scala.collection.mutable.ArrayBuffer[String] = {
    var strat = scala.collection.mutable.ArrayBuffer.empty[String]
    for player <- Players.getGamePlayers do
      strat += player.getPlayerStrategy.toString()
    strat
  }

  /** Returns an ArrayBuffer that contains the hands of every player
    */
  def hand_strings: scala.collection.mutable.ArrayBuffer[List[Card]] = {
    PlayerHands.showString_arr
  }

  /** Returns an Array that contains the cards displayed on the board as a
    * String.
    */
  def board_cards: Array[Card] =
    Board.getBoard

  /** Returns the Pot on the board as a String.
    */
  def getPot: String =
    PotBoard.showString

  /** Flips the randomize flag to either shuffle the deck or keep it
    * non-shuffled.def
    */
  def setShuffle: Unit =
    Deck.randomize

  /** Returns the winner of a hand as a String.
    */
  def getHandFlag: String = Flags.getHandWinner

}
