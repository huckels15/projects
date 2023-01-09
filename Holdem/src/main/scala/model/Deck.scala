package model

import scala.collection.mutable.Stack
import scala.util.Random

/** A deck of cards in the game poker. This is the main deck that players
  * collect from.
  * @constructor
  *   creates an array of ranks, suits, and builds a deck with all cards.
  */
object Deck {
  private val rank: Array[String] =
    Array[String]("A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K")
  private val suit: Array[Char] = Array[Char]('H', 'D', 'C', 'S')
  private var stack: Stack[Card] = new Stack[Card]()
  private var shuffleBool: Boolean = false
  buildDeck()

  /** Randomly shuffles a deck.
    * @return
    *   Unit.
    */
  private def shuffle(): Unit = {
    val rand = if (!shuffleBool) new Random(40L) else new Random()
    stack = rand.shuffle(stack)
  }

  /** Puts cards in the deck and will shuffle them.
    * @return
    *   Unit.
    */
  def buildDeck(): Unit = {
    if (stack.nonEmpty) stack.removeAll()
    for (suits <- suit) {
      for (ranks <- rank) {
        stack.push(new Card(ranks, suits, false))
      }
    }
    shuffle()
  }

  /** Deals a card.
    * @return
    *   A card.
    */
  def deal(): Card = stack.pop()

  def randomize: Unit =
    if shuffleBool == true then shuffleBool = false
    else shuffleBool = true
}
