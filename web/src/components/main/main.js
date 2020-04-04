import React, { useState, useEffect } from 'react'
import { Heading, Box, Select, Text } from 'grommet'
import CountyChart from '../county_chart/county_chart'


const HEADER_TEXT = "COVID-19 Data At A County Level"
const DESCRIPTION = "It can be difficult to wrap your head around the staggering number of cases in the country. "
const DESCRIPTION_2 = "This website shows the number of coronavirus cases and deaths in your county, as well as the total hospital bed capacity "
const DESCRIPTION_3 = "so that you can better understand your local situation. One thing to keep in mind is that not all hospital beds are empty "
const DESCRIPTION_4 = "and not all cases will be hospitalized, so there isn't a 1-1 correspondence between cases and beds. "
const DESCRIPTION_5 = "The hospital data is from 2017, so these numbers may be slightly different than the current data. "
const DESCRIPTION_6 = "Regardless, we hope this does give you a better understanding of your local situation."
const Main = () => {
    const data_url_prefix = `${process.env.REACT_APP_BACKEND}`
    const [states, setStates] = useState([""])
    const [counties, setCounties] = useState([""])
    const [state, setState] = useState('California')
    const [stateUrl, setStateUrl] = useState('California')
    const [county, setCounty] = useState('San Francisco')
    const [countyUrl, setCountyUrl] = useState('SanFrancisco')

    useEffect(() => {
        fetchCounties()
        fetchStates()
    }, [state, county])


    const fetchCounties = () => {
        const data_url = `${data_url_prefix}/${stateUrl}/counties`
        fetch(data_url)
            .then((response) => {
                return response.json()
            }).then((counties) => {
                setCounties(counties)
            })
    }

    const fetchStates = () => {
        const data_url = `${data_url_prefix}/states`
        fetch(data_url)
            .then((response) => {
                return response.json()
            }).then((states) => {
                setStates(states)
            })

    }



    const changeCounty = (e) => {
        setCounty(e.option)
        setCountyUrl(e.option.replace(/\s+/g, ''))
    }

    const changeState = (e) => {
        setState(e.option)
        setCountyUrl('')
        setCounty('')
        setStateUrl(e.option.replace(/\s+/g, ''))
        fetchCounties()
    }

    return (
        <div>
            <Box align='center' gap="medium">
                <Box align='center' width="50vw">
                    <Heading>
                        {HEADER_TEXT}
                    </Heading>
                    <Text>
                        {DESCRIPTION}
                        {DESCRIPTION_2}
                        {DESCRIPTION_3}
                        {DESCRIPTION_4}
                        {DESCRIPTION_5}
                        {DESCRIPTION_6}
                    </Text>
                </Box>
                <Box direction="row" gap="medium">
                    <Select options={states} onChange={changeState} value={state} />
                    <Select options={counties} onChange={changeCounty} value={county} />
                </Box>
            </Box>
            <div>
                <CountyChart state={stateUrl} county={countyUrl} />
            </div>
        </div>
    )
}

export default Main;