import App from "next/app";
import Head from "next/head";
import React from "react";
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import styled, { ThemeProvider, createGlobalStyle } from "styled-components";
import { CssBaseline } from "@mui/material";

const theme = {
  dark: "#262832",
  lessDark: "#313440",
  light: "white",
  lessLight: "whitesmoke",
  reactBlue: "#5fdafb",
  size: {
    xs: "0.25rem",
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
    xl: "2rem"
  }
};

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    font-size: 14px;
    color: ${p => p.theme.dark};
    line-height: 20px;
    font-family: "Lato", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: flex;
    justify-content: center;
    background-color: ${p => p.theme.lessLight};
  }
`;

const Page = styled.div`
  max-width: 800px;
  min-height: 100vh;
`;

const Main = styled.main`
  background-color: ${p => p.theme.light};
  padding: ${p => p.theme.size.lg} ${p => p.theme.size.xl}
    ${p => p.theme.size.md} ${p => p.theme.size.xl};
`;

export default class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props;
    return (
      <>
        <CssBaseline />
        <ThemeProvider theme={theme}>
          <GlobalStyle />
          <Head>
            <title>Gospel Search</title>
            <meta name="viewport" content="initial-scale=1, width=device-width" />
          </Head>
          <Page>
            <Main>
              <Component {...pageProps} />
            </Main>
          </Page>
        </ThemeProvider>
      </>
    );
  }
}
