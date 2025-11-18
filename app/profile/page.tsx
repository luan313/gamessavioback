import { NavHeader } from '@/components/nav-header'
import { ReviewCard } from '@/components/review-card'
import { GameCard } from '@/components/game-card'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Settings, Star, Bell, Calendar } from 'lucide-react'
import Link from 'next/link'

// Mock user data
const userData = {
  name: 'João Silva',
  username: 'joaosilva',
  avatar: '/diverse-user-avatars.png',
  bio: 'Gamer apaixonado por RPGs e jogos indie. Sempre procurando as melhores ofertas.',
  joinDate: 'Janeiro 2023',
  stats: {
    totalReviews: 45,
    averageRating: 8.2,
    gamesWatched: 12,
    followersCount: 234,
  },
}

const userReviews = [
  {
    id: '1',
    userName: 'João Silva',
    userAvatar: '/diverse-user-avatars.png',
    rating: 10,
    comment: 'Uma obra-prima absoluta. A narrativa é envolvente, os personagens são profundos e o gameplay é impecável.',
    createdAt: 'há 2 dias',
    likes: 24,
    isOwnReview: true,
  },
  {
    id: '2',
    userName: 'João Silva',
    userAvatar: '/diverse-user-avatars.png',
    rating: 9,
    comment: 'Jogo incrível com gráficos de última geração e história emocionante.',
    createdAt: 'há 5 dias',
    likes: 18,
    isOwnReview: true,
  },
  {
    id: '3',
    userName: 'João Silva',
    userAvatar: '/diverse-user-avatars.png',
    rating: 8,
    comment: 'Muito bom, mas com alguns problemas de performance.',
    createdAt: 'há 1 semana',
    likes: 12,
    isOwnReview: true,
  },
]

const watchedGames = [
  { id: '7', name: 'Hollow Knight', coverImage: '/hollow-knight-game-cover.jpg', averageRating: 9.0, currentPrice: 7.49, priceDown: true, categories: ['Plataforma', 'Indie'] },
  { id: '8', name: 'Hades', coverImage: '/hades-game-cover.png', averageRating: 9.1, currentPrice: 12.49, priceDown: true, categories: ['Roguelike', 'Ação'] },
  { id: '11', name: 'GTA VI', coverImage: '/gta-6-game-cover.jpg', averageRating: 8.0, currentPrice: 69.99, categories: ['Ação', 'Aventura'] },
  { id: '6', name: 'Cyberpunk 2077', coverImage: '/cyberpunk-game-cover.png', averageRating: 8.5, currentPrice: 29.99, categories: ['RPG', 'Ação'] },
]

export default function ProfilePage() {
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
                  <Link href="/settings">
                    <Button variant="outline" className="gap-2">
                      <Settings className="h-4 w-4" />
                      Editar Perfil
                    </Button>
                  </Link>
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
            <TabsTrigger value="watchlist">Monitorados</TabsTrigger>
          </TabsList>
          
          <TabsContent value="reviews" className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Minhas Avaliações</h2>
              <Badge variant="secondary">{userData.stats.totalReviews} avaliações</Badge>
            </div>
            {userReviews.map((review) => (
              <ReviewCard key={review.id} {...review} />
            ))}
          </TabsContent>
          
          <TabsContent value="watchlist" className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Jogos Monitorados</h2>
              <Badge variant="secondary">{userData.stats.gamesWatched} jogos</Badge>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {watchedGames.map((game) => (
                <GameCard key={game.id} {...game} />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
