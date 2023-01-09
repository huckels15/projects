package controller

import scala.swing._
import controller._
import view._
import model._
import scala.collection.mutable.ArrayBuffer

/** The controller in the MVC architecture.
  * @param view
  *   the view to be controlled
  * @param model
  *   the model to be used to pull data and functions
  */
class Controller(view: View, model: Model) {

  /** Function to run all the necessary functions to update the GUI through the
    * duration of the game.
    */
  def run: Unit =
    view.mod_text(view.p1_score, model.ind_players(0))
    view.mod_text(view.p2_score, model.ind_players(1))
    view.mod_text(view.p3_score, model.ind_players(2))
    view.mod_text(view.p4_score, model.ind_players(3))
    view.mod_menu(view.menu1, model.strats(0))
    view.mod_menu(view.menu2, model.strats(1))
    view.mod_menu(view.menu3, model.strats(2))
    view.mod_menu(view.menu4, model.strats(3))
    view.mod_text(view.p1_strat, model.strats(0))
    view.mod_text(view.p2_strat, model.strats(1))
    view.mod_text(view.p3_strat, model.strats(2))
    view.mod_text(view.p4_strat, model.strats(3))
    view.playerHands(0).showCards(model.hand_strings(0))
    view.playerHands(1).showCards(model.hand_strings(1))
    view.playerHands(2).showCards(model.hand_strings(2))
    view.playerHands(3).showCards(model.hand_strings(3))
    view.flippedCard1.changeCard(model.board_cards(0))
    view.flippedCard2.changeCard(model.board_cards(1))
    view.flippedCard3.changeCard(model.board_cards(2))
    view.flippedCard4.changeCard(model.board_cards(3))
    view.flippedCard5.changeCard(model.board_cards(4))
    view.mod_text(view.pot, model.getPot)
    if model.getHandFlag != "" then
      view.frame.handWinnerAlarm(model.getHandFlag)
      Flags.setHandWinner("")
      view.update
    else if model.checkForWinner != "none" then
      view.frame.winnerAlarm(model.checkForWinner)
      view.update
    view.update

  /** Function to run all the necessary functions to update the GUI when the
    * game ends.
    */
  def dontRun: Unit =
    view.mod_text(view.p1_score, model.ind_players(0))
    view.mod_text(view.p2_score, model.ind_players(1))
    view.mod_text(view.p3_score, model.ind_players(2))
    view.mod_text(view.p4_score, model.ind_players(3))
    view.mod_text(view.p1_strat, model.strats(0))
    view.mod_text(view.p2_strat, model.strats(1))
    view.mod_text(view.p3_strat, model.strats(2))
    view.mod_text(view.p4_strat, model.strats(3))
    view.playerHands(0).showCards(model.hand_strings(0))
    view.playerHands(1).showCards(model.hand_strings(1))
    view.playerHands(2).showCards(model.hand_strings(2))
    view.playerHands(3).showCards(model.hand_strings(3))
    view.flippedCard1.showAsEmpty
    view.flippedCard2.showAsEmpty
    view.flippedCard3.showAsEmpty
    view.flippedCard4.showAsEmpty
    view.flippedCard5.showAsEmpty
    view.mod_text(view.pot, model.getPot)
    if model.checkForWinner != "none" then
      view.frame.winnerAlarm(model.checkForWinner)
      view.update
    else if model.getHandFlag != "" then
      view.frame.handWinnerAlarm(model.getHandFlag)
      Flags.setHandWinner("")
      view.update
    view.update

  /** Initializes Holdem and passes the game area back to the view.
    */
  def initGame: Unit = {
    model.init
    run
  }

  /** Does a move and passes the game area back to the view.
    */
  def move: Unit = {
    model.doMove
    if model.checkForWinner == "none" then run
    else dontRun

  }

  /** Does a turn and passes the game area back to the view.
    */
  def turn: Unit = {
    model.doTurn
    if model.checkForWinner == "none" then run
    else dontRun

  }

  /** Finishes the game and passes the game area back to the view.
    */
  def game: Unit = {
    model.doGame
    dontRun
  }

  /** Toggles the deck to be shuffled randomly
    */
  def random: Unit = {
    model.setShuffle
  }

  /** Exits the view and stops the Holdem program.
    */
  def exit: Unit = {
    sys.exit(0)
  }

  /** Sets the player strategy to default
    * @param player
    *   Player whose strategy is being changed
    */
  def setDefault(player: Player): Unit = {
    player.setPlayerStrategy("followTheLeader")
    run
  }

  /** Sets the player strategy to highCard
    * @param player
    *   Player whose strategy is being changed
    */
  def setHighcard(player: Player): Unit = {
    player.setPlayerStrategy("highCard")
    run
  }

  /** Sets the player strategy to connectors
    * @param player
    *   Player whose strategy is being changed
    */
  def setConnectors(player: Player): Unit = {
    player.setPlayerStrategy("connectors")
    run
  }

  /** Sets the player strategy to aPair
    * @param player
    *   Player whose strategy is being changed
    */
  def setPair(player: Player): Unit = {
    player.setPlayerStrategy("aPair")
    run
  }

}
