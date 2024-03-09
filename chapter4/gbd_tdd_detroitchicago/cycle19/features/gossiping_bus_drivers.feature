Feature: Gossiping bus drivers

  Scenario: Bus drivers successfully share all rumors
    Given maximum number of bus stops driven is 100
    Given bus drivers with the following routes and rumors
      | Route                                   | Rumors                 |
      | stop-a, stop-b, stop-c                  | rumor1, rumor2         |
      | stop-d, stop-b, stop-e                  | rumor1, rumor3, rumor4 |
      | stop-f, stop-g, stop-h, stop-i, stop-e  | rumor1, rumor5, rumor6 |

    When bus drivers have completed driving
    Then all rumors are successfully shared


  Scenario: Bus drivers fails to share all rumors due to driving maximum number of stops
    Given maximum number of bus stops driven is 5
    Given bus drivers with the following routes and rumors
      | Route                                   | Rumors                 |
      | stop-a, stop-b, stop-c                  | rumor1, rumor2         |
      | stop-d, stop-b, stop-e                  | rumor1, rumor3, rumor4 |
      | stop-f, stop-g, stop-h, stop-i, stop-e  | rumor1, rumor5, rumor6 |

      When bus drivers have completed driving
      Then all rumors are not shared


  Scenario: Bus drivers fail to share all rumors because bus routes never cross
     Given maximum number of bus stops driven is 100
     Given bus drivers with the following routes and rumors
       | Route                    | Rumors                 |
       | stop-a, stop-b, stop-c   | rumor1, rumor2         |
       | stop-d, stop-e, stop-f   | rumor1, rumor3, rumor4 |

     When bus drivers have completed driving
     Then all rumors are not shared