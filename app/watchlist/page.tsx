import { NavHeader } from '@/components/nav-header'
import { WatchlistItem } from '@/components/watchlist-item'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Bell, TrendingDown, DollarSign, Target } from 'lucide-react'
import Link from 'next/link'

// Mock data
const watchlistGames = [
  {
    id: '1',
    gameId: '7',
    gameName: 'Hollow Knight',
    gameCover: '/hollow-knight-game-cover.jpg',
    currentPrice: 7.49,
    targetPrice: 10.00,
    lowestPrice: 5.99,
    addedDate: 'há 3 dias',
  },
  {
    id: '2',
    gameId: '8',
    gameName: 'Hades',
    gameCover: '/hades-game-cover.png',
    currentPrice: 12.49,
    targetPrice: 9.99,
    lowestPrice: 9.99,
    addedDate: 'há 1 semana',
  },
  {
    id: '3',
    gameId: '11',
    gameName: 'GTA VI',
    gameCover: '/gta-6-game-cover.jpg',
    currentPrice: 69.99,
    targetPrice: 59.99,
    lowestPrice: 69.99,
    addedDate: 'há 2 semanas',
  },
  {
    id: '4',
    gameId: '6',
    gameName: 'Cyberpunk 2077',
    gameCover: '/cyberpunk-game-cover.png',
    currentPrice: 29.99,
    targetPrice: 35.00,
    lowestPrice: 19.99,
    addedDate: 'há 1 mês',
  },
]

const stats = {
  totalWatched: watchlistGames.length,
  belowTarget: watchlistGames.filter(g => g.currentPrice <= g.targetPrice).length,
  potentialSavings: watchlistGames.reduce((acc, g) => {
    const saving = g.currentPrice - g.lowestPrice
    return acc + (saving > 0 ? saving : 0)
  }, 0),
}

export default function WatchlistPage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">Minha Watchlist</h1>
            <p className="text-muted-foreground">
              Monitore os preços dos seus jogos favoritos
            </p>
          </div>
          <Link href="/games">
            <Button>
              <Bell className="h-4 w-4 mr-2" />
              Adicionar Jogo
            </Button>
          </Link>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Jogos Monitorados</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalWatched}</div>
              <p className="text-xs text-muted-foreground">
                Total na sua watchlist
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Abaixo da Meta</CardTitle>
              <TrendingDown className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-accent">{stats.belowTarget}</div>
              <p className="text-xs text-muted-foreground">
                Jogos no preço desejado
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Economia Potencial</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${stats.potentialSavings.toFixed(2)}</div>
              <p className="text-xs text-muted-foreground">
                Vs. preço mais baixo histórico
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Watchlist Items */}
        {watchlistGames.length > 0 ? (
          <div className="space-y-4">
            {watchlistGames.map((game) => (
              <WatchlistItem key={game.id} {...game} />
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Bell className="h-16 w-16 text-muted-foreground mb-4" />
              <h3 className="text-xl font-semibold mb-2">Nenhum jogo monitorado</h3>
              <p className="text-muted-foreground text-center mb-6">
                Comece a adicionar jogos à sua watchlist para monitorar preços
              </p>
              <Link href="/games">
                <Button>Explorar Jogos</Button>
              </Link>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}
