import React, { useState, useEffect } from 'react'
import { Heading, Box, Select, Text, Footer } from 'grommet'
import CountyChart from '../county_chart/county_chart'


const HEADER_TEXT = "COVID-19 Data At A County Level"
const DESCRIPTION = "It can be difficult to wrap your head around the staggering number of cases in the country. "
const DESCRIPTION_2 = "This website shows the number of coronavirus cases and deaths in your county, as well as the total hospital bed capacity "
const DESCRIPTION_3 = "so that you can better understand your local situation. "
const DESCRIPTION_4 = "One thing to keep in mind is that not all hospital beds are emptyand not all cases will be hospitalized, so there isn't a 1-1 correspondence between cases and beds. "
const DESCRIPTION_5 = "The hospital data is from 2017, so these numbers may be slightly different than the current data. "
const DESCRIPTION_6 = "Regardless, hopefully this does help provide some information."
const FOOTER_TEXT = "Code and data sources available on "
const GITHUB = "Github."
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
        setCountyUrl(e.option.toLowerCase().replace(/\s+/g, ''))
    }

    const changeState = (e) => {
        setState(e.option)
        setCountyUrl('')
        setCounty('')
        setStateUrl(e.option.toLowerCase().replace(/\s+/g, ''))
        fetchCounties()
    }

    const filterState = (e) => {
        console.log(e)
        const filteredStates = states.filter((s) => s.includes(e))
        setStates(filteredStates)
    }

    return (
        <div>
            <Box align='center' gap="medium">
                <Box align='center' width="50vw">
                    <Heading>
                        {HEADER_TEXT}
                    </Heading>
                </Box>
                <Box direction="row" gap="medium">
                    <Select options={states} onChange={changeState} value={state} />
                    <Select options={counties} onChange={changeCounty} value={county} />
                </Box>
            </Box>
            <div>
                <CountyChart state={stateUrl} county={countyUrl} />
            </div>
            <Box align='center' gap="small" margin={{ "top": "medium" }}>
                <Box align='center' width="50vw">
                    <Text>
                        {DESCRIPTION}
                        {DESCRIPTION_2}
                        {DESCRIPTION_3}
                    </Text>
                </Box>
                <Box align='center' width="50vw">
                    <Text>
                        {DESCRIPTION_4}
                        {DESCRIPTION_5}
                        {DESCRIPTION_6}
                    </Text>
                </Box>
                <Footer>
                    <Text>
                        {FOOTER_TEXT}
                        <a href="https://github.com/abhishyantkhare/covid-county-focus">{GITHUB}</a>
                    </Text>
                </Footer>
            </Box>
        </div>
    )
}

export default Main;