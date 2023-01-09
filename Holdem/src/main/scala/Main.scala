import model._
import view._
import controller._

/** The object for the game of Holdem
  */
object Holdem {

  /** Runs the game of Holdem.
    */
  @main def main(): Unit = {

    val model = new Model
    val view = new View
    val controller = new Controller(view, model)

    view.init(controller)
  }

}
