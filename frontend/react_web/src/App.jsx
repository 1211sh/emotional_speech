import { makeStyles } from '@material-ui/styles'
import React from 'react'

import TextInput from './textInput'
import EmotionSlider from './EmotionSlider'
import logo from './emotion_chart.png'
import './App.css'

const useStyles = makeStyles((theme) => ({
  app: {
    alignItems: 'center'
  }
}))

function App() {
  const classes = useStyles()

  return (
    <div className={classes.app}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Emotion - Slider</p>

        <TextInput asd="aa" />
        <br></br>
        <br></br>
        <EmotionSlider />
      </header>
    </div>
  )
}

export default App
