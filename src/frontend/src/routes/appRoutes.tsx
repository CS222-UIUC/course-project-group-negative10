import ReviewsPageLayout from "../pages/reviews/ReviewsPageLayout";
import HomePage from "../pages/home/HomePage";
import { RouteType } from "./config";
import ReviewsOverTime from "../pages/reviews/ReviewsOverTime";
import SettingsPage from "../pages/settings/SettingsPage";
import SentimentAnalysis from "../pages/reviews/SentimentAnalysis";
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';
import ArticleOutlinedIcon from '@mui/icons-material/ArticleOutlined';
import FormatListBulletedOutlinedIcon from '@mui/icons-material/FormatListBulletedOutlined';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';
import AppDetails from "../pages/myapps/AppDetails";
import DownloadsPage from "../pages/downloads/DownloadsPage";

const appRoutes: RouteType[] = [
  {
    index: true,
    element: <HomePage />,
    state: "home"
  },
  {
    path: "/myapps",
    element: <AppDetails />,
    state: "myapps",
    sidebarProps: {
      displayText: "App Details",
      icon: <FileDownloadOutlinedIcon />
    }
  },
  {
    path: "/reviews",
    element: <ReviewsPageLayout />,
    state: "reviews",
    sidebarProps: {
      displayText: "Reviews",
      icon: <DashboardOutlinedIcon />
    },
    child: [
      {
        path: "/reviews/ReviewsOverTime",
        element: <ReviewsOverTime />,
        state: "dashboard.ReviewsOverTime",
        sidebarProps: {
          displayText: "Reviews Graph"
        },
      },
      {
        path: "/reviews/sentimentAnalysis",
        element: <SentimentAnalysis />,
        state: "dashboard.SentimentAnalysis",
        sidebarProps: {
          displayText: "Sentiment Analysis"
        }
      }
    ]
  },
  {
    path: "/Downloads",
    element: <DownloadsPage />,
    state: "DownloadsPage",
    sidebarProps: {
      displayText: "Downloads",
      icon: <ArticleOutlinedIcon />
    }
  },
  {
    path: "/Settings",
    element: <SettingsPage />,
    state: "settings",
    sidebarProps: {
      displayText: "Settings",
      icon: <FormatListBulletedOutlinedIcon />
    }
  }
];

export default appRoutes;