import { NavHeader } from '@/components/nav-header'
import { ReviewCard } from '@/components/review-card'
import { GameCard } from '@/components/game-card'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Calendar, UserPlus } from 'lucide-react'

// Mock user data for other user's profile
const userData = {
  name: 'Maria Santos',
  username: 'mariasantos',
  avatar: '/diverse-user-avatars.png',
  bio: 'Entusiasta de jogos de aventura e puzzles. Amo explorar mundos virtuais.',
  joinDate: 'Março 2023',
  stats: {
    totalReviews: 28,
    averageRating: 8.7,
    gamesWatched: 8,
    followersCount: 156,
  },
  isFollowing: false,
}

const userReviews = [
  {
    id: '1',
    userName: 'Maria Santos',
    userAvatar: '/diverse-user-avatars.png',
    rating: 9,
    comment: 'Jogo incrível com gráficos de última geração e história emocionante. Apenas alguns problemas de ritmo no meio do jogo.',
    createdAt: 'há 3 dias',
    likes: 18,
    isOwnReview: false,
  },
  {
    id: '2',
    userName: 'Maria Santos',
    userAvatar: '/diverse-user-avatars.png',
    rating: 10,
    comment: 'Obra-prima dos jogos indie. Uma experiência única e emocionante.',
    createdAt: 'há 1 semana',
    likes: 32,
    isOwnReview: false,
  },
]

const favoriteGames = [
  { id: '1', name: 'The Last of Us Part II', coverImage: '/the-last-of-us-game-cover.jpg', averageRating: 9.5, currentPrice: 39.99, categories: ['Ação', 'Aventura'] },
  { id: '7', name: 'Hollow Knight', coverImage: '/hollow-knight-game-cover.jpg', averageRating: 9.0, currentPrice: 7.49, priceDown: true, categories: ['Plataforma', 'Indie'] },
  { id: '9', name: 'Stardew Valley', coverImage: '/stardew-valley-game-cover.png', averageRating: 9.3, currentPrice: 9.99, priceDown: true, categories: ['Simulação', 'Indie'] },
]

export default function UserProfilePage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        {/* Profile Header */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row gap-6">
              <Avatar className="h-32 w-32 ring-4 ring-primary/20">
                <AvatarImage src={userData.avatar || "/placeholder.svg"} alt={userData.name} />
                <AvatarFallback className="text-3xl">{userData.name.slice(0, 2).toUpperCase()}</AvatarFallback>
              </Avatar>
              
              <div className="flex-1">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h1 className="text-3xl font-bold mb-1">{userData.name}</h1>
                    <p className="text-muted-foreground">@{userData.username}</p>
                  </div>
                  <Button className="gap-2">
                    <UserPlus className="h-4 w-4" />
                    {userData.isFollowing ? 'Seguindo' : 'Seguir'}
                  </Button>
                </div>
                
                <p className="text-foreground mb-4 leading-relaxed">{userData.bio}</p>
                
                <div className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                  <Calendar className="h-4 w-4" />
                  <span>Membro desde {userData.joinDate}</span>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-3 rounded-lg bg-muted">
                    <div className="text-2xl font-bold">{userData.stats.totalReviews}</div>
                    <div className="text-xs text-muted-foreground">Avaliações</div>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-muted">
                    <div className="text-2xl font-bold">{userData.stats.averageRating}</div>
                    <div className="text-xs text-muted-foreground">Nota Média</div>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-muted">
                    <div className="text-2xl font-bold">{userData.stats.gamesWatched}</div>
                    <div className="text-xs text-muted-foreground">Monitorados</div>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-muted">
                    <div className="text-2xl font-bold">{userData.stats.followersCount}</div>
                    <div className="text-xs text-muted-foreground">Seguidores</div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tabs */}
        <Tabs defaultValue="reviews" className="space-y-6">
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="reviews">Avaliações</TabsTrigger>
            <TabsTrigger value="favorites">Favoritos</TabsTrigger>
          </TabsList>
          
          <TabsContent value="reviews" className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Avaliações de {userData.name}</h2>
              <Badge variant="secondary">{userData.stats.totalReviews} avaliações</Badge>
            </div>
            {userReviews.map((review) => (
              <ReviewCard key={review.id} {...review} />
            ))}
          </TabsContent>
          
          <TabsContent value="favorites" className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Jogos Favoritos</h2>
              <Badge variant="secondary">{favoriteGames.length} jogos</Badge>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {favoriteGames.map((game) => (
                <GameCard key={game.id} {...game} />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
