val scala3Version = "3.1.0"

lazy val root = project
  .in(file("."))
  .settings(
    name := "holdem",
    version := "0.0.1",

    scalaVersion := scala3Version,  

    libraryDependencies ++= Seq(
    "org.scalatest" %% "scalatest" % "3.2.10" % "test",
    "org.scala-lang.modules" %% "scala-swing" % "3.0.0"
    )

  )
