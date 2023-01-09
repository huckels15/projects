package model

import org.scalatest.funspec.AnyFunSpec
import org.scalatest.matchers.should._
import controller._
import model._
import view._
class Model_Test extends AnyFunSpec with Matchers {
  class Fixture {
    val model = new Model
  }
  def fixture = new Fixture
  describe("The Texas Hold 'em simulation") {
    describe("has a Model") {
      // Show Player Order
      it("that can show the player order") {
        val f = fixture
        val expectedResult = "Jacob, John, Bob, Tom"
        f.model.showPlayerOrder shouldBe expectedResult
      }

      // Advance Order
      it("that can advance the player order") {
        val f = fixture
        val expectedResult_0 = "Jacob, John, Bob, Tom"
        val expectedResult_1 = "John, Bob, Tom, Jacob"
        val expectedResult_2 = "Bob, Tom, Jacob, John"
        val expectedResult_3 = "Tom, Jacob, John, Bob"
        val expectedResult_4 = "Jacob, John, Bob, Tom"
        f.model.showPlayerOrder shouldBe expectedResult_0

        f.model.advancePlayerOrder // 1 advance
        f.model.showPlayerOrder shouldBe expectedResult_1

        f.model.advancePlayerOrder // 2 advance
        f.model.showPlayerOrder shouldBe expectedResult_2

        f.model.advancePlayerOrder // 3 advance
        f.model.showPlayerOrder shouldBe expectedResult_3

        f.model.advancePlayerOrder // 4 advance
        f.model.showPlayerOrder shouldBe expectedResult_4
        f.model.showPlayerOrder shouldBe expectedResult_0
      }

      it(
        "and can show the game area, including the cards on the board, players money, players hands, and money in the pot."
      ) {
        val f = fixture
        val expectedResult1 =
          "Board:\n" +
            "null, null, null, null, null\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 1000, John = 1000, Bob = 1000, Tom = 1000\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (), Bob = (), Tom = ()\n" +
            "\n" +
            "Current Pot Size: 0\n"
        f.model.showGameArea shouldBe expectedResult1
      }

      // Check INIT
      it(
        "can INITIALIZE to cause the game board to be cleared and player data reset"
      ) {
        val f = fixture
        Dealer.deal
        Board.fillGameBoard()
        PlayerOrder.current.bet(500)
        PlayerOrder.current.doFold()
        PlayerOrder.foreach(player => player.bet(100))
        Board.getBoard(3).flip()
        Board.getBoard(4).flip()
        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, 5H, 9S\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 500, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 800\n"
        f.model.showGameArea shouldBe expectedResult1

        f.model.init

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"
        f.model.showGameArea shouldBe expectedResult2
      }

      // Check if there is a winner
      it("can CHECK FOR WINNER to show whether a player has won the game") {
        val f = fixture
        f.model.checkForWinner shouldBe "none"

        PlayerOrder.foreach(player => player.setMoney(0))
        PlayerOrder.current.setMoney(4000)
        f.model.checkForWinner shouldBe "Jacob"
      }

      // Test the DO MOVE
      it(
        "can DO MOVE, causing the player at the front of the player order to bet"
      ) {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        f.model.doMove

        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 250\n"

        f.model.showGameArea shouldBe expectedResult1

        val expectedResult_PO_1 = "John, Bob, Tom, Jacob"
        f.model.showPlayerOrder shouldBe expectedResult_PO_1

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 400\n"

        val expectedResult_PO_2 = "Jacob, John, Bob, Tom"

        f.model.doMove
        f.model.doMove
        f.model.doMove

        f.model.showGameArea shouldBe expectedResult2
        f.model.showPlayerOrder shouldBe expectedResult_PO_2
      }
      // TEST DO MOVE IF EVERYONE IS JUST BETTING
      it("can DO MOVE, causing the player at the front of the order to check") {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        Flags.setPreviousDecision("check")

        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult1

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.doMove
        f.model.doMove
        f.model.doMove
        f.model.doMove

        val expectedResult_PO_2 = "Jacob, John, Bob, Tom"
        f.model.showGameArea shouldBe expectedResult2
        f.model.showPlayerOrder shouldBe expectedResult_PO_2
      }

      // Test DO MOVE IF EVERYONE FOLDS
      it("can DO MOVE, causing the player at the front of the order to fold") {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        Flags.setPreviousDecision("fold")
        val expectedResult0 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult0

        f.model.doMove
        val expectedResult_PO_1 = "John, Bob, Tom"
        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"
        f.model.showGameArea shouldBe expectedResult1
        f.model.showPlayerOrder shouldBe expectedResult_PO_1

        f.model.doMove
        val expectedResult_PO_2 = "Bob, Tom"
        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"
        f.model.showPlayerOrder shouldBe expectedResult_PO_2
        f.model.showGameArea shouldBe expectedResult2

        f.model.doMove
        val expectedResult_PO_3 = "Tom"
        val expectedResult3 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (), Bob = (), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"
        f.model.showPlayerOrder shouldBe expectedResult_PO_3
        f.model.showGameArea shouldBe expectedResult3
        // f.model.doMove

        val expectedResult_PO_4 = "Tom"
        val expectedResult4 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (), Bob = (), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"
        f.model.showPlayerOrder shouldBe expectedResult_PO_4
        // f.model.showGameArea shouldBe expectedResult4
      }

      it(
        "can DO TURN to perform DO MOVE four times, unless game has been won when betting"
      ) {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        val expectedResult =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult

        val expectedResult_turn2 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 400\n"

        f.model.doTurn
        f.model.showGameArea shouldBe expectedResult_turn2

        val expectedResult_turn3 =
          "Board:\n" +
            "AS, JC, 8H, 5H, 9S\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 850, John = 850, Bob = 850, Tom = 850\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 600\n"

        f.model.doTurn
        f.model.showGameArea shouldBe expectedResult_turn3
        val expectedResult_turn4 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 750, John = 750, Bob = 1350, Tom = 750\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 400\n"

        f.model.doTurn
        f.model.showGameArea shouldBe expectedResult_turn4

        val expectedResult_turn5 =
          "Board:\n" +
            "AS, JC, 8H, 5H, 9S\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 700, John = 700, Bob = 1300, Tom = 700\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 600\n"

        f.model.doTurn
        f.model.showGameArea shouldBe expectedResult_turn5

        val expectedResult_turn6 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 600, John = 600, Bob = 1800, Tom = 600\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 400\n"

        f.model.doTurn
        f.model.showGameArea shouldBe expectedResult_turn6
      }

      it(
        "can DO TURN to perform DO MOVE four times, unless game has been won when folding"
      ) {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        Flags.setPreviousDecision("fold")
        val expectedResult0 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"
        f.model.showGameArea shouldBe expectedResult0

        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 900, Tom = 1100\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.doTurn
        f.model.showGameArea shouldBe expectedResult1
      }

      it(
        "can DO TURN to perform DO MOVE four times when there are less players in game, unless game has been won when betting"
      ) {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        PlayerOrder.current.doFold()
        Flags.setPreviousDecision("bet")
        val expectedResult0 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult0
        f.model.doTurn

        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 350\n"

        f.model.showGameArea shouldBe expectedResult1

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, 5H, 9S\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 850, Bob = 850, Tom = 850\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 500\n"

        f.model.doTurn

        f.model.showGameArea shouldBe expectedResult2

      }

      it(
        "can DO TURN to perform DO MOVE four times when there are less players in game, unless game has been won when folding"
      ) {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        PlayerOrder.current.doFold()
        val expectedResult0 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult0
        f.model.doTurn

        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 900, Tom = 1100\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult1

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 850, John = 850, Bob = 850, Tom = 1250\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.doTurn

        f.model.showGameArea shouldBe expectedResult2

      }
      it("can DO GAME to perform DO TURN until game is won") {
        val f = fixture
        f.model.init
        for (player <- PlayerOrder) {
          player.setPlayerStrategy("followTheLeader")
        }
        val expectedResult =
          "Board:\n" +
            "null, null, null, null, null\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 0, John = 0, Bob = 4000, Tom = 0\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (), John = (), Bob = (), Tom = ()\n" +
            "\n" +
            "Current Pot Size: 0\n"

        f.model.doGame

        f.model.showGameArea shouldBe expectedResult
      }

      it("can set [player] [strategy]") {
        val f = fixture
        f.model.init
        PlayerOrder.head.setPlayerStrategy("highCard")
        val expectedResult = "highCard"
        PlayerOrder.head.getPlayerStrategy.toString() shouldBe expectedResult

        PlayerOrder.head.setPlayerStrategy("aPair")
        val expectedResult0 = "aPair"
        PlayerOrder.head.getPlayerStrategy.toString() shouldBe expectedResult0
      }

      it("can show strategies") {
        val f = fixture
        f.model.init
        val expectedResult =
          "Jacob: default\n" +
            "John: default\n" +
            "Bob: default\n" +
            "Tom: default\n"
        f.model.showStrategies shouldBe expectedResult

        PlayerOrder.current.setPlayerStrategy("highCard")
        val expectedResult0 =
          "Jacob: highCard\n" +
            "John: default\n" +
            "Bob: default\n" +
            "Tom: default\n"
        f.model.showStrategies shouldBe expectedResult0

        PlayerOrder.advancePlayerOrder()
        PlayerOrder.current.setPlayerStrategy("aPair")

        val expectedResult1 =
          "John: aPair\n" +
            "Bob: default\n" +
            "Tom: default\n" +
            "Jacob: highCard\n"

        f.model.showStrategies shouldBe expectedResult1
      }
      it("can DO MOVE when the first player is using strategy 2") {
        val f = fixture
        f.model.init
        PlayerOrder.current.setPlayerStrategy("highCard")
        val expectedResult0 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult0

        f.model.doMove
        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 250\n"

        f.model.showGameArea shouldBe expectedResult1

        f.model.doMove
        f.model.doMove
        f.model.doMove
        f.model.doMove

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 400\n"

        f.model.showGameArea shouldBe expectedResult2

        // Ensure strategy works when some player folds
        f.model.init
        PlayerOrder.current.setPlayerStrategy("highCard")
        f.model.doMove
        f.model.doMove
        PlayerOrder.current.doFold()
        f.model.doMove
        // f.model.doMove
        val expectedResult3 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (), Tom = ()\n" +
            "\n" +
            "Current Pot Size: 300\n"

        f.model.showGameArea shouldBe expectedResult3
      }

      it("can DO MOVE when the first player is using strategy 3") {
        val f = fixture
        f.model.init
        PlayerOrder.current.setPlayerStrategy("aPair")
        PlayerOrder.current.changeCurrentHand(
          List(new Card("A", 'H'), new Card("A", 'D'))
        )

        val expectedResult =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (AH, AD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult

        f.model.doMove

        val expectedResult0 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (AH, AD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 250\n"

        f.model.showGameArea shouldBe expectedResult0

        f.model.doMove
        f.model.doMove
        f.model.doMove
        f.model.doMove

        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 850, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (AH, AD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 450\n"

        f.model.showGameArea shouldBe expectedResult1

        f.model.init
        f.model.doMove
        f.model.doMove
        PlayerOrder.current.setPlayerStrategy("aPair")
        PlayerOrder.current.changeCurrentHand(
          List(new Card("2", 'H'), new Card("10", 'D'))
        )

        f.model.doMove
        f.model.doMove

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (), Tom = ()\n" +
            "\n" +
            "Current Pot Size: 300\n"

        f.model.showGameArea shouldBe expectedResult2
        // Ensure the case that they check if they do not have a pair
        f.model.init
        PlayerOrder.current.setPlayerStrategy("aPair")
        val expectedResult3 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult3

        f.model.doMove
        f.model.doMove
        f.model.doMove
        f.model.doMove

        val expectedResult4 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult4
      }
      it("can DO MOVE when the first player is using strategy 4.") {
        val f = fixture
        f.model.init
        PlayerOrder.current.setPlayerStrategy("connectors")
        PlayerOrder.current.changeCurrentHand(
          List(new Card("K", 'H'), new Card("A", 'D'))
        )

        val expectedResult =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, AD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult

        f.model.doMove

        val expectedResult0 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, AD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 250\n"

        f.model.showGameArea shouldBe expectedResult0

        f.model.doMove
        f.model.doMove
        f.model.doMove
        f.model.doMove

        val expectedResult1 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, AD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 400\n"

        f.model.showGameArea shouldBe expectedResult1

        PlayerOrder.current.bet(50) // John raises

        f.model.doMove
        f.model.doMove
        f.model.doMove

        val expectedResult2 =
          "Board:\n" +
            "AS, JC, 8H, 5H, 9S\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 800, Bob = 850, Tom = 850\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, AD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 600\n"

        f.model.showGameArea shouldBe expectedResult2

        // Ensure the case that they check if they do not have connecters
        f.model.init
        val expectedResult3 =
          "Board:\n" +
            "AS, JC, 8H, HIDDEN, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 950, John = 950, Bob = 950, Tom = 950\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 200\n"

        f.model.showGameArea shouldBe expectedResult3

        f.model.doMove
        f.model.doMove
        f.model.doMove
        f.model.doMove

        val expectedResult4 =
          "Board:\n" +
            "AS, JC, 8H, 5H, HIDDEN\n" +
            "\n" +
            "Player's Money:\n" +
            "Jacob = 900, John = 900, Bob = 900, Tom = 900\n" +
            "\n" +
            "Player's Hands:\n" +
            "Jacob = (KH, QD), John = (7H, 7D), Bob = (6H, 8C), Tom = (QS, 4H)\n" +
            "\n" +
            "Current Pot Size: 400\n"

        f.model.showGameArea shouldBe expectedResult4
      }
    }
  }
}
