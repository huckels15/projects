package view

import model._
import controller._

import scala.swing._
import BorderPanel.Position._
import java.awt.geom.Rectangle2D
import java.awt.geom.Ellipse2D
import java.awt.Color
import scala.collection.mutable.ArrayBuffer
import java.awt.image.BufferedImage
import scala.swing.Orientation

/** Create a new view.
  * @constructor
  *   create a new Option[Controller] and a text area.
  */
class View {

  // Components

  var _controller: Option[Controller] = None
  var model: Option[Model] = None

  var p1_score = new Label("") {
    background = Color.red
  }
  var p2_score = new Label("") {
    background = Color.red
  }
  var p3_score = new Label("") {
    background = Color.red
  }
  var p4_score = new Label("") {
    background = Color.red
  }
  var p1_strat = new Label("") {
    background = Color.red
  }
  var p2_strat = new Label("") {
    background = Color.red
  }
  var p3_strat = new Label("") {
    background = Color.red
  }
  var p4_strat = new Label("") {
    background = Color.red
  }
  var pot = new Label("") {
    background = Color.red
  }

  val playerHands = new PlayerHands

  val menu1 = new Menu_init(0).menu
  val menu2 = new Menu_init(1).menu
  val menu3 = new Menu_init(2).menu
  val menu4 = new Menu_init(3).menu

  val menuBar1 = new MenuBar {
    contents += menu1
  }
  val menuBar2 = new MenuBar {
    contents += menu2
  }
  val menuBar3 = new MenuBar {
    contents += menu3
  }
  val menuBar4 = new MenuBar {
    contents += menu4
  }

  val buttons = new Button_panel()

  var my_label = new Label("Scoreboard") {
    background = Color.red
    opaque = true
  }

  val scoreboard = new GridPanel(6, 3) {

    contents += my_label
    contents += new Label("Hands") {
      background = Color.red
      opaque = true
    }
    contents += new Label("Strategy") {
      background = Color.red
      opaque = true
    }

    contents += p1_score
    contents += playerHands(0)
    contents += menuBar1
    contents += p2_score
    contents += playerHands(1)
    contents += menuBar2
    contents += p3_score
    contents += playerHands(2)
    contents += menuBar3
    contents += p4_score
    contents += playerHands(3)
    contents += menuBar4
    contents += pot
    background = Color.red
    contents += new TextArea("") { background = Color.red }
    contents += new TextArea("") { background = Color.red }
  }

  var flippedCard1 = new CardPanel
  var flippedCard2 = new CardPanel
  var flippedCard3 = new CardPanel
  var flippedCard4 = new CardPanel
  var flippedCard5 = new CardPanel

  val board_cards = new BoxPanel(Orientation.Horizontal) {
    contents += flippedCard1
    contents += flippedCard2
    contents += flippedCard3
    contents += flippedCard4
    contents += flippedCard5
  }

  val area = new BorderPanel {
    background = Color.white
    layout += buttons -> West
    layout += scoreboard -> South
    layout += board_cards -> Center
  }

  val frame = new MyFrame

  // End of Components

  // View Classes and Functions

  /** Initializs the view.
    * @param controller
    */
  def init(controller: Controller): Unit = {
    _controller = Some(controller)
  }

  /** Class for the down menus displayed in the GUI.
    * @param ind
    *   The index of the player who's strategy is being affected.
    */
  class Menu_init(ind: Int) {
    val menu = new Menu("Default") {
      contents += new MenuItem(Action("Default") {
        _controller.get.setDefault(Players.getGamePlayers(ind))
      })
      contents += new MenuItem(Action("High Card") {
        _controller.get.setHighcard(Players.getGamePlayers(ind))
      })
      contents += new MenuItem(Action("Connectors") {
        _controller.get.setConnectors(Players.getGamePlayers(ind))
      })
      contents += new MenuItem(Action("A Pair") {
        _controller.get.setPair(Players.getGamePlayers(ind))
      })
    }
  }

  /** Class for the menu command buttons in a BoxPanel.
    */
  class Button_panel extends BoxPanel(Orientation.Vertical) {
    contents += new Button(Action("Initialize        ") {
      _controller.get.initGame
    })
    contents += new Button(Action("Do move       ") {
      _controller.get.move
    })
    contents += new Button(Action("Do turn          ") {
      _controller.get.turn
    })
    contents += new Button(Action("Do game       ") {
      _controller.get.game
    })
    contents += new Button(Action("Randomize   ") {
      _controller.get.random
    })
    contents += new Button(Action("Exit                ") {
      _controller.get.exit
    })

    background = Color.black
  }

  /** Class for the cards shown on the board.
    */
  class CardPanel extends Panel {

    var image =
      javax.imageio.ImageIO.read(new java.io.File("resources/empty.jpg"))
    var back =
      javax.imageio.ImageIO.read(new java.io.File("resources/felt.jpg"))

    /** Shows cards on board as empty.
      */
    def showAsEmpty: Unit = {
      image =
        javax.imageio.ImageIO.read(new java.io.File("resources/empty.jpg"))
      this.repaint()
    }

    /** Changes cards displayed on the board.
      * @param card
      *   The card to be placed on the board
      */
    def changeCard(card: Card): Unit = {
      if !card.getFlipped then
        image = javax.imageio.ImageIO.read(
          new java.io.File(
            "resources/" + card.getRank + card.getSuit.toLower.toString + ".jpg"
          )
        )
      else
        image =
          javax.imageio.ImageIO.read(new java.io.File("resources/back.jpg"))
      this.repaint()
    }

    /** Paints the card images onto the board.
      */
    override def paint(g: Graphics2D): Unit = {
      g.drawImage(back, 0, 0, null)
      g.drawImage(image, 18, 48, null)
    }
  }

  /** Class for the cards shown in player hands.
    */
  class PlayerHandPanel(orientation: Char) extends Panel {

    preferredSize = new Dimension(5, 5)

    var images = new ArrayBuffer[BufferedImage]
    images += javax.imageio.ImageIO.read(
      new java.io.File("resources/empty.jpg")
    )

    /** Shows cards in players hands as empty.
      */
    def showAsEmpty: Unit = {
      images.clear
      images += javax.imageio.ImageIO.read(
        new java.io.File("resources/empty.jpg")
      )
      this.repaint()
    }

    /** Shows cards in players hands.
      * @param cards
      *   The list of cards a player posseses
      */
    def showCards(cards: List[Card]): Unit = {
      images.clear
      for (card <- cards) {
        images += javax.imageio.ImageIO.read(
          new java.io.File(
            "resources/" + card.getRank + card.getSuit.toString + ".jpg"
          )
        )
      }
      super.repaint()
    }

    /** Paints the players hands onto the grid panel.
      */
    override def paint(g: Graphics2D): Unit = {
      var offset = 0
      for (image <- images) {
        if (orientation == 'v') g.drawImage(image, 0, offset, null)
        else g.drawImage(image, offset, 0, null)
        offset += 90
      }
    }
  }

  /** Class for organizing player hands.
    */
  class PlayerHands extends ArrayBuffer[PlayerHandPanel] {

    this += new PlayerHandPanel('h')
    this += new PlayerHandPanel('h')
    this += new PlayerHandPanel('h')
    this += new PlayerHandPanel('h')

    /** Resets player hands.
      */
    def reset: Unit = {
      for panel <- this yield panel.showAsEmpty
    }
  }

  /** Class to create the MainFrame.
    */
  class MyFrame extends MainFrame {

    /** Displays pop up when the game has been won
      * @param player
      *   The player who has won
      */
    def winnerAlarm(player: String) =
      Dialog.showMessage(
        this,
        player + " has won!",
        title = "Winner!"
      )

    /** Displays pop up when the hand has been won
      * @param player
      *   The player who has won
      */
    def handWinnerAlarm(player: String) =
      Dialog.showMessage(
        this,
        player + " has won the hand!",
        title = "Hand winner!"
      )

    preferredSize = new Dimension(600, 600)
    title = "Hold em'"
    contents = area
    centerOnScreen()
    visible = true
  }

  /** Allows other classes to modify the text area.
    * @param label
    *   The label to be modified
    * @param str
    *   The string to be placed in the label's text
    */
  def mod_text(label: Label, str: String): Unit =
    label.text = str

  /** Allows other classes to modify the menus.
    * @param menu
    *   The menu to be modified
    * @param str
    *   The string to be placed in the Menu's text
    */
  def mod_menu(menu: Menu, str: String): Unit =
    menu.text = str

  /** Updates the view.
    */
  def update: Unit = {
    frame.repaint()
    for (panel <- playerHands) panel.repaint()
  }

}
