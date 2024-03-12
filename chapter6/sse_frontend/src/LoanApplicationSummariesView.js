import React, { useEffect, useState } from 'react';

export default function LoanApplicationSummariesView() {
  const [ loanAppSummaries, setLoanAppSummaries ] = useState([]);

  // Define an effect to be executed on component mount
  useEffect(() => {
    // Create new event source
    // Hardcoded dev environment URL is used here for demonstration
    // purposes
    const eventSource =
        new EventSource('http://localhost:8000/subscribe-to-loan-app-summaries');

    // Listen to server sent events and add a new
    // loan application summary to the head of
    // loanAppSummaries array
    eventSource.addEventListener('message', (messageEvent) => {
      try {
        const loanAppSummary = JSON.parse(messageEvent.data);

        if (loanAppSummary) {
          setLoanAppSummaries([loanAppSummary, ...loanAppSummaries]);
        }
      } catch {
        // Handle error
      }
    });


    eventSource.addEventListener('error', (errorEvent) => {
      // Handle error
    });

    // Close the event source on component unmount
    return function cleanup() { eventSource.close(); }
  }, [loanAppSummaries]);

  // Render loan application summary list items
  const loanAppSummaryListItems =
      loanAppSummaries.map(({id}) =>
          (<li key={id}>{id}</li>));

  return (
      <ul>{loanAppSummaryListItems}</ul>
  );
}
