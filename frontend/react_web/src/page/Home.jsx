import { makeStyles } from '@material-ui/core/styles'
import React from 'react'

import Inference from './inference/Inference'
import Intro from './intro/Intro'
import TitleBar from './titlebar/TitleBar'
import PhotoPage from './photoPage/PhotoPage'
import TimeLine from './timeline/TimeLine'

const useStyles = makeStyles({
  root: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%'
  },
  content: {
    marginTop: 80
  }
})

export default function Home() {
  const classes = useStyles()
  //const focusName = useState('intro')
  //const ref = useRef()

  // const handleFocus = useCallback((event) => {
  //   event.preventDefault()
  //   switch(param){
  //     case '':
  //       return <Intro/>
  //     case '':
  //       return <Inference/>
  //     case '':
  //       return <TimeLine/>
  //     case '':
  //       return <PhotoPage/>
  // }
  //   ref.focus()
  // }, [ref1, ref2, ref3, ref4])

  

  return (
    <div className={classes.root}>
      <TitleBar />
      <div className={classes.content}>
        <Intro />
        <Inference />
        <TimeLine />
        <PhotoPage />
      </div>
    </div>
  )
}
